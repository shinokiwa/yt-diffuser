/**
 * composables/api/sse/message.js のテスト
 */
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mount } from "@vue/test-utils";

import { useMessage } from "@/composables/api/sse/message";
import { useNotificationStore } from "@/composables/store/notification";

// モックの設定
vi.mock("@/composables/store/notification", () => {
    const enqueue = vi.fn();
    const useNotificationStore = vi.fn(() => ({ toast: { enqueue } }));
    return {
        useNotificationStore,
    };
});

describe("useMessage", () => {
    let eventSourceMock;

    beforeEach(() => {
        // EventSourceのモックを設定
        eventSourceMock = {
            onmessage: null,
            close: vi.fn(),
        };
        window.EventSource = vi.fn(() => eventSourceMock);
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it("mount時にEventSourceが開始される", () => {
        mount({
            setup() {
                return useMessage();
            },
        });

        expect(window.EventSource).toHaveBeenCalledWith("/api/sse/message");
    });

    it("EventSource.onmessageでメッセージを処理する", () => {
        const wrapper = mount({
            setup() {
                return useMessage();
            },
        });

        const message = { label: "新しいメッセージ" };
        eventSourceMock.onmessage({ data: JSON.stringify(message) });

        expect(useNotificationStore().toast.enqueue).toHaveBeenCalledWith(
            message.label
        );
    });

    it("unmount時にEventSourceが閉じられる", () => {
        const wrapper = mount({
            setup() {
                return useMessage();
            },
        });

        wrapper.unmount();
        expect(eventSourceMock.close).toHaveBeenCalled();
    });
});

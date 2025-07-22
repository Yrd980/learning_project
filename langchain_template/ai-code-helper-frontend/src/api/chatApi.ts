import axios from "axios";

const API_BASE_URL = "http://localhost:8081/api";

export function chatWithSSE(
  memoryId: number,
  message: string,
  onMessage: (data: string) => void,
  onError?: (error: Event) => void,
  onClose?: () => void,
): EventSource {
  const params = new URLSearchParams({
    memoryId: String(memoryId),
    message: message,
  });

  const eventSource = new EventSource(`${API_BASE_URL}/ai/chat?${params}`);

  eventSource.onmessage = function (event: MessageEvent) {
    const data = event.data;
    if (data && data.trim() !== "") {
      onMessage(data);
    }
  };

  eventSource.onerror = function (error: Event) {
    if (eventSource.readyState !== EventSource.CLOSED) {
      onError && onError(error);
    }
    if (eventSource.readyState !== EventSource.CLOSED) {
      eventSource.close();
    }
  };

  eventSource.onclose = function () {
    onClose && onClose();
  };

  return eventSource;
}

export async function checkServiceHealth(): Promise<boolean> {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`, {
      timeout: 5000,
    });
    return response.status === 200;
  } catch (error) {
    return false;
  }
}

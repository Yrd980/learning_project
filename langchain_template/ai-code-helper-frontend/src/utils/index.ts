export function generateMemoryId(): number {
  return Math.floor(Date.now() % 1000000000);
}

export function formatTime(date: Date): string {
  const now = new Date();
  const diff = now.getTime() - date.getTime();

  if (diff < 60000) {
    return "just now";
  } else if (diff < 3600000) {
    return `${Math.floor(diff / 60000)} minutes ago`;
  } else if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)} hours ago`;
  } else {
    return date.toLocaleDateString();
  }
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number,
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;
  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

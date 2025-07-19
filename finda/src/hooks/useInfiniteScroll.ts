import { useCallback, useRef } from "react";

export function useInfiniteScroll({
  loading,
  hasMore,
  onLoadMore,
}: {
  loading: boolean;
  hasMore: boolean;
  onLoadMore: () => void;
}) {
  const observer = useRef<IntersectionObserver | null>(null);
  const lastElementRef = useCallback(
    (node: Element | null) => {
      if (loading) return;
      if (observer.current) observer.current.disconnect();
      observer.current = new window.IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && hasMore) {
          onLoadMore();
        }
      });
      if (node) observer.current.observe(node);
    },
    [loading, hasMore, onLoadMore],
  );
  return lastElementRef;
}


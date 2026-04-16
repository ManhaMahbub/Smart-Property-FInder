import heapq


def astar_rank(df):
    """Rank properties using A* heuristic: lower predicted price + distance is better."""
    heap = []

    for i, row in df.iterrows():
        g = row["predicted_price"]
        h = row["distance_to_station"] * 1000
        f = g + h
        heapq.heappush(heap, (f, i))

    ranked_indices = [heapq.heappop(heap)[1] for _ in range(min(10, len(heap)))]
    return df.loc[ranked_indices]

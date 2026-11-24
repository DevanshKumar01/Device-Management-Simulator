class MemoryManager:

    @staticmethod
    def validate(pages, frames):
        if not pages:
            raise ValueError("Page reference string cannot be empty")

        if not isinstance(frames, int) or frames <= 0:
            raise ValueError("Frames must be a positive integer")

        if any(not isinstance(p, int) or p < 0 for p in pages):
            raise ValueError("Page numbers must be non-negative integers")

    @staticmethod
    def simulate(pages, frames, algorithm="FIFO"):
        MemoryManager.validate(pages, frames)

        algorithm = algorithm.strip().upper()

        if algorithm not in ["FIFO", "LRU", "OPTIMAL"]:
            raise ValueError("Invalid page replacement algorithm")

        memory = []
        history = []
        hits = 0
        faults = 0
        last_used = {}

        for index, page in enumerate(pages):

            if page in memory:
                hits += 1
                status = "Hit"

            else:
                faults += 1
                status = "Fault"

                if len(memory) < frames:
                    memory.append(page)

                elif algorithm == "FIFO":
                    memory.pop(0)
                    memory.append(page)

                elif algorithm == "LRU":
                    victim = min(
                        memory,
                        key=lambda p: last_used[p]
                    )

                    memory.remove(victim)
                    memory.append(page)

                elif algorithm == "OPTIMAL":

                    future = pages[index + 1:]

                    def next_use(p):
                        if p in future:
                            return future.index(p)
                        return float("inf")

                    victim = max(memory, key=next_use)

                    memory.remove(victim)
                    memory.append(page)

            last_used[page] = index

            history.append({
                "Step": index + 1,
                "Page": page,
                "Frames": memory.copy(),
                "Status": status
            })

        return {
            "algorithm": algorithm,
            "total_references": len(pages),
            "page_hits": hits,
            "page_faults": faults,
            "hit_ratio": round(hits / len(pages) * 100, 2),
            "fault_ratio": round(faults / len(pages) * 100, 2),
            "history": history
        }

    @staticmethod
    def compare(pages, frames):
        results = []

        for algorithm in ["FIFO", "LRU", "OPTIMAL"]:

            result = MemoryManager.simulate(
                pages, frames, algorithm
            )

            results.append({
                "Algorithm": algorithm,
                "Page Hits": result["page_hits"],
                "Page Faults": result["page_faults"],
                "Hit Ratio (%)": result["hit_ratio"],
                "Fault Ratio (%)": result["fault_ratio"]
            })

        return results
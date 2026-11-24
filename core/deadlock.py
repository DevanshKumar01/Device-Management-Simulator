class DeadlockManager:

    @staticmethod
    def validate(allocation, maximum, available):

        if not allocation or not maximum or not available:
            raise ValueError("Input matrices cannot be empty")

        if len(allocation) != len(maximum):
            raise ValueError("Process count mismatch")

        resources = len(available)

        for matrix in [allocation, maximum]:
            for row in matrix:
                if len(row) != resources:
                    raise ValueError("Resource count mismatch")

                if any(type(x) is not int or x < 0 for x in row):
                    raise ValueError("Invalid resource values")

        if any(type(x) is not int or x < 0 for x in available):
            raise ValueError("Invalid available resources")

        for i in range(len(allocation)):
            for j in range(resources):
                if allocation[i][j] > maximum[i][j]:
                    raise ValueError(
                        "Allocation cannot exceed maximum demand"
                    )

    @staticmethod
    def bankers_algorithm(allocation, maximum, available):

        DeadlockManager.validate(
            allocation, maximum, available
        )

        n = len(allocation)
        m = len(available)

        need = [
            [
                maximum[i][j] - allocation[i][j]
                for j in range(m)
            ]
            for i in range(n)
        ]

        work = available.copy()
        finished = [False] * n
        safe_sequence = []
        history = []

        while len(safe_sequence) < n:

            found = False

            for i in range(n):

                if not finished[i] and all(
                    need[i][j] <= work[j]
                    for j in range(m)
                ):

                    before = work.copy()

                    for j in range(m):
                        work[j] += allocation[i][j]

                    finished[i] = True
                    safe_sequence.append(f"P{i}")

                    history.append({
                        "Step": len(safe_sequence),
                        "Process": f"P{i}",
                        "Available Before": before,
                        "Released Resources": allocation[i].copy(),
                        "Available After": work.copy()
                    })

                    found = True

            if not found:
                break

        safe = all(finished)

        unfinished = [
            f"P{i}"
            for i in range(n)
            if not finished[i]
        ]

        return {
            "safe": safe,
            "status": "Safe State" if safe else "Unsafe State",
            "need": need,
            "safe_sequence": safe_sequence if safe else [],
            "partial_sequence": safe_sequence,
            "unfinished_processes": unfinished,
            "final_available": work,
            "history": history
        }
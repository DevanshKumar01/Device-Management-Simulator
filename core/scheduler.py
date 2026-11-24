class Scheduler:

    @staticmethod
    def fcfs(queue):
        """First Come First Serve Scheduling."""
        if not queue:
            return None

        return queue.popleft()

    @staticmethod
    def priority(queue):
        """Lower number means higher priority."""
        if not queue:
            return None

        selected = min(
            queue,
            key=lambda request: request["priority"]
        )

        queue.remove(selected)

        return selected

    @staticmethod
    def get_next_request(queue, algorithm="FCFS"):
        algorithm = algorithm.strip().upper()

        if algorithm == "FCFS":
            return Scheduler.fcfs(queue)

        elif algorithm == "PRIORITY":
            return Scheduler.priority(queue)

        else:
            raise ValueError("Invalid scheduling algorithm")
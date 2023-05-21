from fetcher.fetcher import ClassroomFetcher, IHomeworkFetcher

if __name__ == "__main__":
    fetcher: IHomeworkFetcher = ClassroomFetcher()
    fetcher.get_assignment_submissions("NTk1MzUxNTE3MjE4", "NjA3NzgzMTUwODg5")

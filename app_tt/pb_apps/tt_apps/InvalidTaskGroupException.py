
"""
 Exception of Invalid Task Group, must
 launched when the task group don't have
 all tasks completed to create a new task.
"""
class InvalidTaskGroupException(Exception):
    def __init__(self):
        pass
    
    def __str__(self):
        return "Invalid Task Group Exception"
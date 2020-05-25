from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        self.command = None

    def next_command(self, command):
        self.command = command
        return self

    @staticmethod
    def validate(**kwargs):
        data = kwargs.get('data')
        if not data:
            kwargs['data'] = {}

        response = kwargs.get('response')
        if not response:
            kwargs['response'] = {}

        return kwargs

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplementedError('Must implement that subclass')


class CommandInitializer:
    def __init__(self, commands):
        self.exec_command = None
        prev_command = None

        for command_ins in commands:
            current_command = command_ins()
            if not self.exec_command:
                self.exec_command = current_command

            if not prev_command:
                prev_command = current_command
            else:
                prev_command.next_command(current_command)
                prev_command = current_command

    def execute(self, **kwargs):
        if self.exec_command:
            return self.exec_command.execute(**kwargs)
        return None, None


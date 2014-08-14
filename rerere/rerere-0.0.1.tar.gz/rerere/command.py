# -*- coding: utf-8 -*-
import abc


class CommandException(Exception):
    def __init__(self, message):
        self.message = message


class Command(object, metaclass=abc.ABCMeta):
    """
    コマンドを表します
    """

    command_name = None
    pair_command_name = None
    is_block_command = False
    is_block_start = False
    parent_block_command_ids = []

    def __init__(self, command_manager, text_manager, line):
        self.command_manager = command_manager
        self.text_manager = text_manager
        self.keys = line.get('keys', [])
        self.pattern = line.get('attributes', {}).get('pattern', '')
        self.command_id = line.get('attributes', {}).get('id', '')
        self.search_mode = line.get('attributes', {}).get('search_mode', '')
        self.attributes = line.get('attributes', {})
        self.line = line.get('line', '')
        self.unmatch_count = 0

    def __repr__(self):
        ret = self.command_name
        ret += ' / keys:' + ','.join(self.keys)
        ret += ' / pattern:' + self.pattern
        ret += ' / command_id:' + self.command_id
        ret += ' / parent_block_command_ids:' + ','.join(self.parent_block_command_ids)
        ret += '\n'
        return ret

    @abc.abstractmethod
    def start(self):
        """
        コマンドマネージャがこのコマンドにカーソルを合わせたときに呼ばれる関数。
        正規表現としての評価はまだ実施されていません。
        @return 評価するコマンドリストのカーソルを次行へ進めて再帰的にコマンド構築処理をする場合True
        """
        pass

    @abc.abstractmethod
    def match(self, search):
        """
        マッチしたときに呼ばれる関数。
        @param search マッチしたオブジェクト
        @return 評価対象のテキストのカーソルを次行へ進める場合True
        """
        pass

    @abc.abstractmethod
    def unmatch(self):
        """
        マッチしなかったときに呼ばれる関数。
        @return 評価対象のテキストのカーソルを次行へ進める場合True
        """
        pass

    @abc.abstractmethod
    def remain(self):
        """
        テキストの評価が最後まで行ったときに、コマンドが残っていたときに呼ばれる関数。
        @return テキストの評価を再開する場合True
        """
        pass


class Anycommand(Command):

    command_name = 'any'
    pair_command_name = None
    is_block_command = False
    is_block_start = False

    def start(self):
        return True

    def match(self, search):
        pass

    def unmatch(self):
        pass

    def remain(self):
        pass


class Ifcommand(Command):

    command_name = 'if'
    pair_command_name = 'endif'
    is_block_command = True
    is_block_start = True

    def __init__(self, command_manager, text_manager, line):
        Command.__init__(self, command_manager, text_manager, line)
        if self.attributes.get('match', None):
            self.pattern = self.attributes['match']
        if self.attributes.get('exit', None):
            self.exit = self.attributes['exit']
        if self.attributes.get('limit', None):
            self.limit = int(self.attributes['limit'])
        if self.search_mode == 'single':
            self.limit = 1

        if not self.pattern:
            raise CommandException('Error at line ' + self.line)

    def start(self):
        # textの行を記憶(最悪戻るため)
        self.text_start_line_number = self.text_manager.get_line_number()
        self.command_manager.set_command(self)
        return False

    def match(self, search):
        self.command_manager.remove_command(self)
        self.text_manager.move_index_to_same_line()
        return True

    def __clear(self):
        self.command_manager.move_index_to_pair_command(self)
        self.command_manager.remove_command(self)
        self.command_manager.remove_child_commands(self)
        # txtの評価を無かったことにする
        self.text_manager.set_line_number(self.text_start_line_number)

    def unmatch(self):
        self.unmatch_count += 1

        if hasattr(self, 'limit'):
            if self.text_manager.get_line_number() - self.text_start_line_number >= self.limit:
                self.__clear()
                return True

        # exitのパターンがあったら
        if hasattr(self, 'exit'):
            if self.text_manager.search(self.text_manager.get_current_line(), self.exit):
                self.__clear()
                return True

        return False

    def remain(self):
        self.__clear()
        return True


class Endifcommand(Command):

    command_name = 'endif'
    pair_command_name = 'if'
    is_block_command = True
    is_block_start = False

    def start(self):
        return True

    def match(self, search):
        return True

    def unmatch(self):
        return False

    def remain(self):
        return False


class Blockcommand(Command):

    command_name = 'block'
    pair_command_name = 'endblock'
    is_block_command = True
    is_block_start = True

    def __init__(self, command_manager, text_manager, line):
        Command.__init__(self, command_manager, text_manager, line)
        if self.attributes.get('exit', None):
            self.pattern = self.attributes['exit']

        if not self.pattern:
            raise CommandException('Error at line ' + self.line)

    def start(self):
        self.command_manager.set_command(self)
        return True

    def match(self, search):
        self.command_manager.move_index_to_pair_command(self)
        self.command_manager.remove_command(self)
        self.command_manager.remove_child_commands(self)
        self.text_manager.move_index_to_same_line()
        return True

    def unmatch(self):
        self.unmatch_count += 1
        return False

    def remain(self):
        return False


class Endblockcommand(Command):

    command_name = 'endblock'
    pair_command_name = 'block'
    is_block_command = True
    is_block_start = False

    def start(self):
        return True

    def match(self, search):
        return True

    def unmatch(self):
        return False

    def remain(self):
        return False


class Loopcommand(Command):

    command_name = 'loop'
    pair_command_name = 'endloop'
    is_block_command = True
    is_block_start = True

    def __init__(self, command_manager, text_manager, line):
        Command.__init__(self, command_manager, text_manager, line)
        if self.attributes.get('exit', None):
            self.pattern = self.attributes['exit']

        if not self.pattern:
            raise CommandException('Error at line ' + self.line)

    def start(self):
        self.command_manager.add_loop_counter(self.command_id)
        self.command_manager.set_command(self)
        return True

    def match(self, search):
        self.command_manager.clear_loop_counter(self.command_id)
        self.command_manager.move_index_to_pair_command(self)
        self.command_manager.remove_command(self)
        self.command_manager.remove_child_commands(self)
        self.text_manager.move_index_to_same_line()
        return True

    def unmatch(self):
        self.unmatch_count += 1
        return False

    def remain(self):
        return False


class Endloopcommand(Command):

    command_name = 'endloop'
    pair_command_name = 'loop'
    is_block_command = True
    is_block_start = False

    def start(self):
        # loopの終了合図が見つからないままendに来てしまった。loopの先頭へ戻る
        self.command_manager.add_loop_counter(self.command_id)
        self.command_manager.move_index_to_pair_command(self)
        return True

    def match(self, search):
        return True

    def unmatch(self):
        return False

    def remain(self):
        return False


class Searchcommand(Command):

    command_name = 'search'
    pair_command_name = None
    is_block_command = False

    def __init__(self, command_manager, text_manager, line):
        Command.__init__(self, command_manager, text_manager, line)
        if not self.pattern:
            raise CommandException('Error at line ' + self.line)

    def start(self):
        self.command_manager.set_command(self)
        return False

    def match(self, search):
        if self.keys:
            for i, key in enumerate(self.command_manager.create_keys(self.keys)):
                if '[]' in key:
                    key = key.replace('[]', '')
                    if not key in self.text_manager.ret:
                        self.text_manager.ret[key] = []
                    self.text_manager.ret[key].append(search.group(i + 1))
                elif '+' in key:
                    key = key.replace('+', '')
                    if not key in self.text_manager.ret:
                        self.text_manager.ret[key] = ''
                    self.text_manager.ret[key] += (search.group(i + 1))
                else:
                    self.text_manager.ret[key] = search.group(i + 1)
        self.command_manager.remove_command(self)
        return True

    def unmatch(self):
        self.unmatch_count += 1
        if self.search_mode == 'single':
            self.command_manager.remove_command(self)
            self.text_manager.move_index_to_same_line()
            return True
        elif self.search_mode == 'multi':
            if self.unmatch_count == 1:
                self.text_manager.move_index_to_same_line()
                return True
            else:
                return False

        return False

    def remain(self):
        return False

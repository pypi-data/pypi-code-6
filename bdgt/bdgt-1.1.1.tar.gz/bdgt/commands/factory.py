from bdgt.commands import accounts, budget, importer, transactions


__all__ = ['CommandFactory']


class CommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'command')

        if args.command == 'account':
            return AccountCommandFactory.create(args)
        elif args.command == 'import':
            return ImportCommandFactory.create(args)
        elif args.command == 'tx':
            return TxCommandFactory.create(args)
        elif args.command == 'set':
            return budget.CmdSet(args.category_name, args.period, args.amount)
        elif args.command == 'status':
            return budget.CmdStatus(args.month, args.year)
        else:
            assert False


class AccountCommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')

        if args.sub_command == 'add':
            return accounts.CmdAddAccount(args.name, args.number)
        elif args.sub_command == 'delete':
            return accounts.CmdDeleteAccount(args.name)
        elif args.sub_command == 'list':
            return accounts.CmdListAccounts()
        else:
            assert False


class ImportCommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')

        if args.sub_command == 'add':
            return importer.CmdAdd(args.transaction_ids)
        elif args.sub_command == 'remove':
            return importer.CmdRemove(args.transaction_ids)
        elif args.sub_command == 'reset':
            return importer.CmdReset()
        elif args.sub_command == 'set':
            return importer.CmdSet(args.field, args.value,
                                   args.transaction_ids)
        elif args.sub_command == 'commit':
            return importer.CmdCommit()
        elif args.sub_command == 'file':
            return importer.CmdImport(args.type_, args.file_, args.commit)
        elif args.sub_command == 'status':
            return importer.CmdStatus()
        else:
            assert False


class TxCommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')

        if args.sub_command == 'list':
            return transactions.CmdListTx(args.account_name)
        elif args.sub_command == 'assign':
            return transactions.CmdAssignTx(args.category_name,
                                            args.transaction_ids)
        elif args.sub_command == 'unassign':
            return transactions.CmdUnassignTx(args.transaction_ids)
        elif args.sub_command == 'reconcile':
            return transactions.CmdReconcileTx(args.transaction_ids)
        else:
            assert False

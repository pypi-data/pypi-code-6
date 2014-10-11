from mtk.amqp_0_9_1.gen import Connection
from mtk.amqp_0_9_1.gen import Channel
from mtk.amqp_0_9_1.gen import Exchange
from mtk.amqp_0_9_1.gen import Queue
from mtk.amqp_0_9_1.gen import Basic
from mtk.amqp_0_9_1.gen import Tx

methods = {}
methods[(10,10)] = Connection.Start
methods[(10,11)] = Connection.StartOk
methods[(10,20)] = Connection.Secure
methods[(10,21)] = Connection.SecureOk
methods[(10,30)] = Connection.Tune
methods[(10,31)] = Connection.TuneOk
methods[(10,40)] = Connection.Open
methods[(10,41)] = Connection.OpenOk
methods[(10,50)] = Connection.Close
methods[(10,51)] = Connection.CloseOk
methods[(20,10)] = Channel.Open
methods[(20,11)] = Channel.OpenOk
methods[(20,20)] = Channel.Flow
methods[(20,21)] = Channel.FlowOk
methods[(20,40)] = Channel.Close
methods[(20,41)] = Channel.CloseOk
methods[(40,10)] = Exchange.Declare
methods[(40,11)] = Exchange.DeclareOk
methods[(40,20)] = Exchange.Delete
methods[(40,21)] = Exchange.DeleteOk
methods[(50,10)] = Queue.Declare
methods[(50,11)] = Queue.DeclareOk
methods[(50,20)] = Queue.Bind
methods[(50,21)] = Queue.BindOk
methods[(50,50)] = Queue.Unbind
methods[(50,51)] = Queue.UnbindOk
methods[(50,30)] = Queue.Purge
methods[(50,31)] = Queue.PurgeOk
methods[(50,40)] = Queue.Delete
methods[(50,41)] = Queue.DeleteOk
methods[(60,10)] = Basic.Qos
methods[(60,11)] = Basic.QosOk
methods[(60,20)] = Basic.Consume
methods[(60,21)] = Basic.ConsumeOk
methods[(60,30)] = Basic.Cancel
methods[(60,31)] = Basic.CancelOk
methods[(60,40)] = Basic.Publish
methods[(60,50)] = Basic.Return
methods[(60,60)] = Basic.Deliver
methods[(60,70)] = Basic.Get
methods[(60,71)] = Basic.GetOk
methods[(60,72)] = Basic.GetEmpty
methods[(60,80)] = Basic.Ack
methods[(60,90)] = Basic.Reject
methods[(60,100)] = Basic.RecoverAsync
methods[(60,110)] = Basic.Recover
methods[(60,111)] = Basic.RecoverOk
methods[(90,10)] = Tx.Select
methods[(90,11)] = Tx.SelectOk
methods[(90,20)] = Tx.Commit
methods[(90,21)] = Tx.CommitOk
methods[(90,30)] = Tx.Rollback
methods[(90,31)] = Tx.RollbackOk

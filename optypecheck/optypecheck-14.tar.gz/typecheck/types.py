"""
Created on 30/06/2014
@author: Carlo Pires <carlopires@gmail.com>
"""
NotImplementedCls = NotImplemented.__class__
NoneCls = None.__class__
BooleanCls = bool
StrCls = str
BytesCls = bytes
IntegralCls = 'numbers.Integral' # int
RealCls = 'numbers.Real' # float
DecimalCls = 'decimal.Decimal'
TupleCls = ().__class__
ListCls = [].__class__

HashableCls = 'collections.Hashable'
IterableCls = 'collections.Iterable'
IteratorCls = 'collections.Iterator'
SizedCls = 'collections.Sized'
ContainerCls = 'collections.Container'
CallableCls = 'collections.Callable'
SetCls = 'collections.Set'
MutableSetCls = 'collections.MutableSet'
MappingCls = 'collections.Mapping'
MutableMappingCls = 'collections.MutableMapping'
MappingViewCls = 'collections.MappingView'
KeysViewCls = 'collections.KeysView'
ItemsViewCls = 'collections.ItemsView'
ValuesViewCls = 'collections.ValuesView'
SequenceCls = 'collections.Sequence'
MutableSequenceCls = 'collections.MutableSequence'
ByteStringCls = 'collections.ByteString'

CodeCls = 'types.CodeType'
MethodCls = 'types.MethodType'
GeneratorCls = 'types.GeneratorType'
FunctionCls = 'types.FunctionType'
BuiltinFunctionCls = 'types.BuiltinFunctionType'
MappingProxyCls = 'types.MappingProxyType'
BuiltinMethodCls = 'types.BuiltinMethodType'
ModuleCls = 'types.ModuleType'
FrameCls = 'types.FrameType'
GetSetDescriptorCls = 'types.GetSetDescriptorType'
LambdaCls = 'types.LambdaType'
TracebackCls = 'types.TracebackType'
MemberDescriptorCls = 'types.MemberDescriptorType'

AioLoopCls = 'asyncio.events.AbstractEventLoop'

UUIDCls = 'uuid.UUID'
TimeCls = 'datetime.time'
DateCls = 'datetime.date'
DateTimeCls = 'datetime.datetime'

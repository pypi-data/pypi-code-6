

PROTOCOL_MAJOR = 0
PROTOCOL_MINOR = 9
PROTOCOL_REVISION = 1

PORT = 5672

FRAME_METHOD = 1

FRAME_HEADER = 2

FRAME_BODY = 3

FRAME_HEARTBEAT = 8

FRAME_MIN_SIZE = 4096

FRAME_END = 206

# 
# Indicates that the method completed successfully. This reply code is
# reserved for future use - the current protocol design does not use positive
# confirmation and reply codes are sent only in case of an error.
# 
REPLY_SUCCESS = 200

# 
# The client attempted to transfer content larger than the server could accept
# at the present time. The client may retry at a later time.
# 
CONTENT_TOO_LARGE = 311

# 
# When the exchange cannot deliver to a consumer when the immediate flag is
# set. As a result of pending data on the queue or the absence of any
# consumers of the queue.
# 
NO_CONSUMERS = 313

# 
# An operator intervened to close the connection for some reason. The client
# may retry at some later date.
# 
CONNECTION_FORCED = 320

# 
# The client tried to work with an unknown virtual host.
# 
INVALID_PATH = 402

# 
# The client attempted to work with a server entity to which it has no
# access due to security settings.
# 
ACCESS_REFUSED = 403

# 
# The client attempted to work with a server entity that does not exist.
# 
NOT_FOUND = 404

# 
# The client attempted to work with a server entity to which it has no
# access because another client is working with it.
# 
RESOURCE_LOCKED = 405

# 
# The client requested a method that was not allowed because some precondition
# failed.
# 
PRECONDITION_FAILED = 406

# 
# The sender sent a malformed frame that the recipient could not decode.
# This strongly implies a programming error in the sending peer.
# 
FRAME_ERROR = 501

# 
# The sender sent a frame that contained illegal values for one or more
# fields. This strongly implies a programming error in the sending peer.
# 
SYNTAX_ERROR = 502

# 
# The client sent an invalid sequence of frames, attempting to perform an
# operation that was considered invalid by the server. This usually implies
# a programming error in the client.
# 
COMMAND_INVALID = 503

# 
# The client attempted to work with a channel that had not been correctly
# opened. This most likely indicates a fault in the client layer.
# 
CHANNEL_ERROR = 504

# 
# The peer sent a frame that was not expected, usually in the context of
# a content header and body.  This strongly indicates a fault in the peer's
# content processing.
# 
UNEXPECTED_FRAME = 505

# 
# The server could not complete the method because it lacked sufficient
# resources. This may be due to the client creating too many of some type
# of entity.
# 
RESOURCE_ERROR = 506

# 
# The client tried to work with some entity in a manner that is prohibited
# by the server, due to security settings or by some other criteria.
# 
NOT_ALLOWED = 530

# 
# The client tried to use functionality that is not implemented in the
# server.
# 
NOT_IMPLEMENTED = 540

# 
# The server could not complete the method because of an internal error.
# The server may require intervention by an operator in order to resume
# normal operations.
# 
INTERNAL_ERROR = 541



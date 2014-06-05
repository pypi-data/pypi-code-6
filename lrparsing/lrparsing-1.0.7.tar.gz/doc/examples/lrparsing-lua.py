#!/usr/bin/python -W default
#
# Testing the lua compiler.
#
# Copyright (c) 2013,2014 Russell Stuart.
# Licensed under GPLv2, or any later version.
#
import sys
import time

import lua52


def main(argv=sys.argv):
    grammar = lua52.Lua52Grammar
    if len(argv) == 2 and argv[1] == '--compile':
        start_time = time.time()
        print grammar.pre_compile_grammar(None)
        print "compile time: %f secs" % (time.time() - start_time)
        sys.exit(1)
    start_time = time.time()
    try:
        grammar.compile_grammar()
    except:
        try:
            print grammar.repr_grammar()
            print
            print grammar.repr_productions()
            print
            print grammar.repr_parse_table()
        finally:
            raise
    print "parser generation time: %f secs" % (time.time() - start_time)
    print
    assert not grammar.unused_rules(), grammar.unused_rules()
    start_time = time.time()
    for i in xrange(len(lua_tests)):
        if len(argv) == 1 or argv[1] != '--quiet':
            print grammar.repr_parse_tree(grammar.parse(lua_tests[i]))
            print
    print "avg compile_time=%f" % ((time.time() - start_time) / len(lua_tests))

lua_tests = [
    """
    -- The Computer Language Benchmarks Game
    -- http://benchmarksgame.alioth.debian.org/
    -- contributed by Mike Pall

    local function kfrequency(seq, freq, k, frame)
        local sub = string.sub
        local k1 = k - 1
        for i=frame,string.len(seq)-k1,k do
            local c = sub(seq, i, i+k1)
            freq[c] = freq[c] + 1
        end
    end

    local function freqdefault()
        return 0
    end

    local function count(seq, frag)
        local k = string.len(frag)
        local freq = setmetatable({}, { __index = freqdefault })
        for frame=1,k do kfrequency(seq, freq, k, frame) end
        io.write(freq[frag] or 0, "\t", frag, "\n")
    end

    local function frequency(seq, k)
        local freq = setmetatable({}, { __index = freqdefault })
        for frame=1,k do kfrequency(seq, freq, k, frame) end
        local sfreq, sn = {}, 1
        for c,v in pairs(freq) do sfreq[sn] = c; sn = sn + 1 end
        table.sort(sfreq, function(a, b)
            local fa, fb = freq[a], freq[b]
            return fa == fb and a > b or fa > fb
        end)
        sum = string.len(seq)-k+1
        for _,c in ipairs(sfreq) do
            io.write(string.format("%s %0.3f\n", c, (freq[c]*100)/sum))
        end
        io.write("\n")
    end

    local function readseq()
        local sub = string.sub
        for line in io.lines() do
            if sub(line, 1, 1) == ">" and sub(line, 2, 6) == "THREE" then break end
        end
        local lines, ln = {}, 0
        for line in io.lines() do
            local c = sub(line, 1, 1)
            if c == ">" then
                break
            elseif c ~= ";" then
                ln = ln + 1
                lines[ln] = line
            end
        end
        return string.upper(table.concat(lines, "", 1, ln))
    end

    local seq = readseq()
    frequency(seq, 1)
    frequency(seq, 2)
    count(seq, "GGT")
    count(seq, "GGTA")
    count(seq, "GGTATT")
    count(seq, "GGTATTTTAATT")
    count(seq, "GGTATTTTAATTTATAGT")""",

    # ------------------------------------------------------------------------

    """
    -- classlib.lua 2.04.04
    --
    -- Changes from 2.03:
    --
    -- 1.	Included patches and ideas from Peter Schaefer
    -- 		(peter.schaefer@gmail.com) considerably improving the efficiency of
    -- 		build(), __init() and other parts of the code.
    --
    -- 2.	The former remove_ambiguous() function was removed, improving the
    -- 		efficiency of both build() (instance creation) and mt:__call() (class
    -- 		creation). Ambiguities are now processed using the ambiguous_keys
    -- 		tables introduced by Peter.
    --
    -- 3.	Removed inheritance of class properties, which was inconsistent with
    -- 		the way instance properties are handled (see pages 4-5 of the manual).
    -- 		Mostly harmless, but confusing. Now only methods are inherited.
    --

    -- PRIVATE

    --[[
            Define unique value for identifying ambiguous base objects and inherited
            attributes. Ambiguous values are normally removed from classes and objects,
            but if keep_ambiguous == true they are left there and the ambiguous value
            is made to behave in a way useful for debugging.
    ]]

    local ambiguous

    if keep_ambiguous then

            ambiguous = { _type = 'ambiguous' }

            local function invalid(operation)
                    return function()
                            error('Invalid ' .. operation .. ' on ambiguous')
                    end
            end

            -- Make ambiguous complain about everything except tostring()
            local ambiguous_mt =
            {
                    __add		= invalid('addition'),
                    __sub		= invalid('substraction'),
                    __mul		= invalid('multiplication'),
                    __div		= invalid('division'),
                    __mod		= invalid('modulus operation'),
                    __pow		= invalid('exponentiation'),
                    __unm		= invalid('unary minus'),
                    __concat	= invalid('concatenation'),
                    __len		= invalid('length operation'),
                    __eq		= invalid('equality comparison'),
                    __lt		= invalid('less than'),
                    __le		= invalid('less or equal'),
                    __index		= invalid('indexing'),
                    __newindex	= invalid('new indexing'),
                    __call		= invalid('call'),
                    __tostring	= function() return 'ambiguous' end,
                    __tonumber	= invalid('conversion to number')
            }
            setmetatable(ambiguous, ambiguous_mt)

    end


    --[[
            Reserved attribute names.
    ]]

    local reserved =
    {
            __index			= true,
            __newindex		= true,
            __type			= true,
            __class			= true,
            __bases			= true,
            __inherited		= true,
            __from			= true,
            __shared		= true,
            __user_init		= true,
            __name			= true,
            __initialized	= true
    }

    --[[
            Some special user-set attributes are renamed.
    ]]

    local rename =
    {
            __init	= '__user_init',
            __set	= '__user_set',
            __get	= '__user_get'
    }

    --[[
            The metatable of all classes, containing:

            To be used by the classes:
            __call()		for creating instances
            __init() 		default constructor
            is_a()			for checking object and class types
            implements()	for checking interface support

            For internal use:
            __newindex()	for controlling class population
    ]]

    local class_mt = {}
    class_mt.__index = class_mt

    --[[
            This controls class population.
            Here 'self' is a class being populated by inheritance or by the user.
    ]]

    function class_mt:__newindex(name, value)

            -- Rename special user-set attributes
            if rename[name] then name = rename[name] end

            -- __user_get() needs an __index() handler
            if name == '__user_get' then
                    self.__index = value and function(obj, k)
                            local v = self[k]
                            if v == nil and not reserved[k] then v = value(obj, k) end
                            return v
                    end or self

            -- __user_set() needs a __newindex() handler
            elseif name == '__user_set' then
                    self.__newindex = value and function(obj, k, v)
                            if reserved[k] or not value(obj, k, v) then rawset(obj, k, v) end
                    end or nil

            end

            -- Assign the attribute
            rawset(self, name, value)
    end

    --[[
            This function creates an object of a certain class and calls itself
            recursively to create one child object for each base class. Base objects
            of unnamed base classes are accessed by using the base class as an index
            into the object, base objects of named base classes are accessed as fields
            of the object with the names of their respective base classes.
            Classes derived in shared mode will create only a single base object.
            Unambiguous grandchildren are inherited by the parent if they do not
            collide with direct children.
    ]]

    local function build(class, shared_objs, shared)

            -- If shared, look in the repository of shared objects
            -- and return any previous instance of this class.
            if shared then
                    local prev_instance = shared_objs[class]
                    if prev_instance then return prev_instance end
            end

            -- Create new object
            local obj = { __type = 'object' }

            -- Build child objects if there are base classes
            local nbases = #class.__bases
            if nbases > 0 then

                    -- Repository for storing inherited base objects
                    local inherited = {}

                    -- List of ambiguous keys
                    local ambiguous_keys = {}

                    -- Build child objects for each base class
                    for i = 1, nbases do
                            local base = class.__bases[i]
                            local child = build(base, shared_objs, class.__shared[base])
                            obj[base.__name] = child

                            -- Get inherited grandchildren from this child
                            for c, grandchild in pairs(child) do

                                    -- We can only accept one inherited grandchild of each class,
                                    -- otherwise this is an ambiguous reference
                                    if not ambiguous_keys[c] then
                                            if not inherited[c] then inherited[c] = grandchild
                                            elseif inherited[c] ~= grandchild then
                                                    inherited[c] = ambiguous
                                                    table.insert(ambiguous_keys, c)
                                            end
                                    end
                            end
                    end

                    -- Accept inherited grandchildren if they don't collide with
                    -- direct children
                    for k, v in pairs(inherited) do
                            if not obj[k] then obj[k] = v end
                    end

            end

            -- Object is ready
            setmetatable(obj, class)

            -- If shared, add it to the repository of shared objects
            if shared then shared_objs[class] = obj end

            return obj

    end

    --[[
            The __call() operator creates an instance of the class and initializes it.
    ]]

    function class_mt:__call(...)
            local obj = build(self, {}, false)
            obj:__init(...)
            return obj
    end

    --[[
            The implements() method checks that an object or class supports the
            interface of a target class. This means it can be passed as an argument to
            any function that expects the target class. We consider only functions
            and callable objects to be part of the interface of a class.
    ]]

    function class_mt:implements(class)

            -- Auxiliary function to determine if something is callable
            local function is_callable(v)
                    if v == ambiguous then return false end
                    if type(v) == 'function' then return true end
                    local mt = getmetatable(v)
                    return mt and type(mt.__call) == 'function'
            end

            -- Check we have all the target's callables (except reserved names)
            for k, v in pairs(class) do
                    if not reserved[k] and is_callable(v) and not is_callable(self[k]) then
                            return false
                    end
            end
            return true
    end

    --[[
            The is_a() method checks the type of an object or class starting from
            its class and following the derivation chain upwards looking for
            the target class. If the target class is found, it checks that its
            interface is supported (this may fail in multiple inheritance because
            of ambiguities).
    ]]

    function class_mt:is_a(class)

            -- If our class is the target class this is trivially true
            if self.__class == class then return true end

            -- Auxiliary function to determine if a target class is one of a list of
            -- classes or one of their bases
            local function find(target, classlist)
                    for i = 1, #classlist do
                            local class = classlist[i]
                            if class == target or find(target, class.__bases) then
                                    return true
                            end
                    end
                    return false
            end

            -- Check that we derive from the target
            if not find(class, self.__bases) then return false end

            -- Check that we implement the target's interface.
            return self:implements(class)
    end

    --[[
            Factory-supplied constructor, calls the user-supplied constructor if any,
            then calls the constructors of the bases to initialize those that were
            not initialized before. Objects are initialized exactly once.
    ]]

    function class_mt:__init(...)
            if self.__initialized then return end
            if self.__user_init then self:__user_init(...) end
            for i = 1, #self.__bases do
                    local base = self.__bases[i]
                    self[base.__name]:__init(...)
            end
            self.__initialized = true
    end


    -- PUBLIC

    --[[
            Utility type and interface checking functions
    ]]

    function typeof(value)
            local t = type(value)
            return t =='table' and value.__type or t
    end

    function classof(value)
            local t = type(value)
            return t == 'table' and value.__class or nil
    end

    function classname(value)
            if not classof(value) then return nil end
            local name = value.__name
            return type(name) == 'string' and name or nil
    end

    function implements(value, class)
            return classof(value) and value:implements(class) or false
    end

    function is_a(value, class)
            return classof(value) and value:is_a(class) or false
    end

    --[[
            Use a table to control class creation and naming.
    ]]

    class = {}
    local mt = {}
    setmetatable(class, mt)

    --[[
            Create a named or unnamed class by calling class([name, ] ...).
            Arguments are an optional string to set the class name and the classes or
            shared classes to be derived from.
    ]]

    function mt:__call(...)

            local arg = {...}

            -- Create a new class
            local c =
            {
                    __type = 'class',
                    __bases = {},
                    __shared = {}
            }
            c.__class = c
            c.__index = c

            -- A first string argument sets the name of the class.
            if type(arg[1]) == 'string' then
                    c.__name = arg[1]
                    table.remove(arg, 1)
            else
                    c.__name = c
            end

            -- Repository of inherited attributes
            local inherited = {}
            local from = {}

            -- List of ambiguous keys
            local ambiguous_keys = {}

            -- Inherit from the base classes
            for i = 1, #arg do
                    local base = arg[i]

                    -- Get the base and whether it is inherited in shared mode
                    local basetype = typeof(base)
                    local shared = basetype == 'share'
                    assert(basetype == 'class' or shared,
                                    'Base ' .. i .. ' is not a class or shared class')
                    if shared then base = base.__class end

                    -- Just in case, check this base is not repeated
                    assert(c.__shared[base] == nil, 'Base ' .. i .. ' is duplicated')

                    -- Accept it
                    c.__bases[i] = base
                    c.__shared[base] = shared

                    -- Get methods that could be inherited from this base
                    for k, v in pairs(base) do

                            -- Skip reserved and ambiguous methods
                            if type(v) == 'function' and not reserved[k] and
                                    not ambiguous_keys[k] then

                                    -- Where does this method come from?
                                    local new_from

                                    -- Check if the method was inherited by the base
                                    local base_inherited = base.__inherited[k]
                                    if base_inherited then

                                            -- If it has been redefined, cancel this inheritance
                                            if base_inherited ~= v then		-- (1)
                                                    base.__inherited[k] = nil
                                                    base.__from[k] = nil

                                            -- It is still inherited, get it from the original
                                            else
                                                    new_from = base.__from[k]
                                            end
                                    end

                                    -- If it is not inherited by the base, it originates there
                                    new_from = new_from or { class = base, shared = shared }

                                    -- Accept a first-time inheritance
                                    local current_from = from[k]
                                    if not current_from then
                                            from[k] = new_from
                                            local origin = new_from.class

                                            -- We assume this is an instance method (called with
                                            -- self as first argument) and wrap it so that it will
                                            -- receive the correct base object as self. For class
                                            -- functions this code is unusable.
                                            inherited[k] = function(self, ...)
                                                    return origin[k](self[origin.__name], ...)
                                            end

                                    -- Methods inherited more than once are ambiguous unless
                                    -- they originate in the same shared class.
                                    elseif current_from.class ~= new_from.class or
                                                    not current_from.shared or not new_from.shared then
                                            inherited[k] = ambiguous
                                            table.insert(ambiguous_keys, k)
                                            from[k] = nil
                                    end
                            end
                    end
            end

            -- Set the metatable now, it monitors attribute setting and does some
            -- special processing for some of them.
            setmetatable(c, class_mt)

            -- Set inherited attributes in the class, they may be redefined afterwards
            for k, v in pairs(inherited) do c[k] = v end	-- checked at (1)
            c.__inherited = inherited
            c.__from = from

            return c
    end

    --[[
            Create a named class and assign it to a global variable of the same name.
            Example: class.A(...) is equivalent to (global) A = class('A', ...).
    ]]

    function mt:__index(name)
            return function(...)
                    local c = class(name, ...)
                    getfenv()[name] = c
                    return c
            end
    end

    --[[
            Wrap a class for shared derivation.
    ]]

    function shared(class)
            assert(typeof(class) == 'class', 'Argument is not a class')
            return { __type = 'share', __class = class }
    end
    """,
]


if __name__ == "__main__":
    main(sys.argv)

# vim: set shiftwidth=4 expandtab softtabstop=8 :

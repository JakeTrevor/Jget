do --settings block
    settings.define("JGET.setup",
        { description = "flag that tracks weather jget has injected it's path modification", default = false })
    settings.define("JGET.token", { description = "Token for authenticating actions with JGET", default = "" })
    settings.define("JGET.username", { description = "Username for JGET", default = "" })
    settings.define("JGET.outdir", { description = "Directory packages are installed into", default = "packages/" })
    settings.define("JGET.endpoint",
        { description = "Location of JGET webserver. Uses master server as default",
            default = "https://jget.trevor.business/" })
    settings.define("JGET.use_cache",
        { description = "refer to a cache server (if one exists) for credentials", default = true })
    settings.save()
end

local endpoint = settings.get("JGET.endpoint")
local outdir = settings.get("JGET.outdir")
local user = settings.get("JGET.username")
local token = settings.get("JGET.token")
local use_cache = settings.get("JGET.use_cache")


local function encode64(data)
    local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    return ((data:gsub('.', function(x)
        local r, b = '', x:byte()
        for i = 8, 1, -1 do r = r .. (b % 2 ^ i - b % 2 ^ (i - 1) > 0 and '1' or '0') end
        return r;
    end) .. '0000'):gsub('%d%d%d?%d?%d?%d?', function(x)
        if (#x < 6) then return '' end
        local c = 0
        for i = 1, 6 do c = c + (x:sub(i, i) == '1' and 2 ^ (6 - i) or 0) end
        return b:sub(c + 1, c + 1)
    end) .. ({ '', '==', '=' })[#data % 3 + 1])
end

function Set(list)
    local set = {}
    for _, l in ipairs(list) do set[l] = true end
    return set
end

local function ensure(dirname)
    if not fs.exists(dirname) then
        fs.makeDir(dirname)
    end
end

local function install(dirname, files)
    ensure(dirname)
    for fname, value in pairs(files) do
        local file_path = fs.combine(dirname, fname)
        if type(value) == "string" then
            --its a file
            local file = fs.open(file_path, "w")
            file.write(value)
            file.close()

        else
            --its a directory
            install(file_path, value)
        end

    end
end

local function get_intalled_packages()
    return fs.list(outdir)
end

local function whoami()
    if token then
        print("logged in as " .. user)
    else
        print("not logged in")
    end
end

local function list()
    print("installed packages:")
    print(textutils.serialise(get_intalled_packages()))
end

local function login(...)
    write("username: ")
    local username = read()
    write("password: ")
    local password = read()

    local auth = encode64(username .. ":" .. password)

    local target_url = endpoint .. "auth/api/login/"
    local response, reason, _ = http.post {
        url = target_url, body = "", method = "POST",
        headers = { ["Authorization"] = "Basic " .. auth }
    }

    if not response then
        print("error: " .. reason)
        return
    end

    local data = textutils.unserialiseJSON(response.readAll())
    local token = data["token"]

    settings.set("JGET.token", token)
    settings.set("JGET.username", username)
    settings.save()
    print("login successful")
end

local function get(arg)
    local package = arg[2]

    print("getting package " .. package)

    local target_url = endpoint .. "api/get/" .. package .. "/"

    local headers = {}
    if token then
        headers = { ["Authorization"] = "Token " .. token }
    end

    local response, reason, _ = http.get {
        url = target_url, method = "GET",
        headers = headers
    }

    if not response then
        print("error: " .. reason)
        return
    end

    local data = textutils.unserialiseJSON(response.readAll())
    local files = textutils.unserialiseJSON(data["files"])

    local outdir = shell.resolve(outdir)
    ensure(outdir)

    local install_dir = fs.combine(outdir, package)
    install(install_dir, files)


    local dependencies = data["dependencies"]
    local installed_packages = Set(get_intalled_packages())

    for _, package in ipairs(dependencies) do
        if not installed_packages[package] then
            get({ "", package })
        end
    end

end

local function init()
    write("Package name:")
    local name = read()
    local data = {
        name = name,
        authors = { user },
        dependencies = textutils.empty_json_array
    }

    local json_data = textutils.serialiseJSON(data)

    local file = fs.open(shell.resolve("./package.jget"), "w")
    file.write(json_data)
    file.close()
end

local function addDependencies()

    if not fs.exists(shell.resolve("./package.jget")) then
        print("Please initialise the project first with command 'jget init'")
        return
    end

    local dependencies = get_intalled_packages()

    print("Adding the follwing packages as dependencies:")

    for _, package in ipairs(dependencies) do
        print(package)
    end

    local file = fs.open(shell.resolve("./package.jget"), "r")

    local json_data = file.readAll()
    file.close()

    local data = textutils.unserialiseJSON(json_data)

    data["dependencies"] = dependencies

    local new_json = textutils.serialiseJSON(data)

    file = fs.open(shell.resolve("./package.jget"), "w")

    file.write(new_json)
    file.close()
end

local function get_files(path)
    local data = {}
    local file_names = fs.list(path)
    for _, file_name in ipairs(file_names) do
        if not ((file_name == "package.jget") or (file_name == "packages")) then
            local file_path = fs.combine(path, file_name)
            if fs.isDir(file_path) then
                data[file_name] = get_files(file_path)
            else
                local file = fs.open(file_path, "r")
                data[file_name] = file.readAll()
                file.close()
            end
        end
    end
    return data
end

local function put()
    if not token then
        print("You must be logged in to make put requests")
        print("Log in with 'jget login'")
        return
    end

    if not fs.exists(shell.resolve("./package.jget")) then
        print("This directory is not a package")
        print("Please initialise first with 'jget init'")
        return
    end

    local file = fs.open(shell.resolve("./package.jget"), "r")
    local json_data = file.readAll()
    file.close()

    local data = textutils.unserialiseJSON(json_data)
    --get files
    local current_directory = shell.resolve(".")

    local files = get_files(current_directory)

    data["files"] = textutils.serialiseJSON(files)

    json_data = textutils.serialiseJSON(data)

    --make put request
    local target_url = endpoint .. "api/put/" .. data.name .. "/"

    local args = {
        url = target_url, body = json_data, method = "POST",
        headers = { ["Authorization"] = "Token " .. token, ["Content-Type"] = "application/json" }
    }
    local response, reason, _ = http.post(args)

    if not response then
        print("Error: " .. reason)
        return
    end

    if response.getResponseCode() == 200 then
        print("Package uploaded successfully")
    else
        print("Error: code " .. response.getResponseCode())
    end

end

local function setup()
    if not settings.get("JGET.setup") then
        local injection =
        [[--this section amends the path so that jget packages can be imported without referencing 'packages/'
    shell.setPath(shell.path()..":packages/")
    --amend startup from here
    
    ]]
        local startup_file = fs.open("startup.lua", "r")

        local contents = startup_file.readAll()

        startup_file.close()

        startup_file = fs.open("startup.lua", "w")

        startup_file.write(injection .. contents)

        startup_file.close()

        settings.set("JGET.setup", true)
        settings.save()
    end
end

local help_dict = {
    ["list"] = [[
list
- lists all packages installed in the current directory

useage:
'jget list'
]]   ,
    ["login"] = [[
login
- connects to jget server (defined by endpoint) and requests an authentication token
- this will prompt you for your username and password
- you will need to sign up for a jget account for this - see jget website for details

useage:
'jget login'
]]   ,
    ["whoami"] = [[
whoami
- checks if you are currently logged in (if you have an auth token) and prints the current username
- if you are not logged it, it will also tell you.

useage:
'jget whoami'
]]   ,
    ["get"] = [[
get
- requests the specified package from the jget repo (defined by the endpoint)
- installed the package in the current outdir (by default "./packages/")
- also installs all dependencies of that package.

useage:
'jget get <package name>'
]]   ,
    ["put"] = [[
put
- assuming the current directory is setup as a jget package, it will be uploaded to the jget repo
- this requires you to be logged in (to track ownership), 
- the current directory must be a valid package - see help on 'init'
- if the package already exists on the repo, and the user has editing permissions, then the package will be updated

    useage:
'jget put'
]]   ,
    ["init"] = [[
init
- creates a package.jget file in the current directory which contains information required for uploading
- it will prompt you for a package name; this must be a valid url segment
- this must be done before uploading the package (see 'put') or adding dependencies (see 'addDeps')

useage:
'jget init'
]]   ,
    ["addDeps"] = [[
addDeps
- short for 'add dependencies'
- gets a list of all packages installed in this directory and adds them to the package.jget file as dependencies
- this can only be done if the package is already initialised (see help on 'init')

useage:
'jget addDeps'
]]   ,
    ["help"] = [[
help
- you are already using this command!
- given a command, will print availible help information for that command

useage:
'jget help <command>'
]]   ,
}

local function jget_help(arg)
    local commad = arg[2]
    if help_dict[commad] then
        print()
        print(help_dict[commad])
    else
        print()
        print("Command not recognised. Use 'jget' for list of commands")
        print()
        print("or type 'jget help help' for information on how to use this command")
        print()
    end
end

local commands = {
    ["list"] = list,
    ["login"] = login,
    ["whoami"] = whoami,
    ["get"] = get,
    ["put"] = put,
    ["init"] = init,
    ["addDeps"] = addDependencies,
    ["help"] = jget_help
}


local function main(arg)
    setup()

    local command = arg[1]
    if not command then
        print("")
        print("please enter a command")
        print("one of:")
        print("----")
        for name, _ in pairs(commands) do
            print(name)
        end
        print()
        return
    end

    if commands[command] then
        commands[command](arg)
    else
        print("unrecognised command: " .. command)

    end
end

main(arg)

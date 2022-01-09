local lfs = require("lfs")

path="./"
for file in lfs.dir(path) do
    print(file)
end
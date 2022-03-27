package initialize

import (
	"os"
	"fmt"

    "github.com/fsnotify/fsnotify"
    "github.com/spf13/viper"

    "github.com/x-few/xway/backend/utils"
    "github.com/x-few/xway/backend/config"
)

func Viper(conf *config.Config) *viper.Viper {
    var file string

    if fileEnv := os.Getenv(utils.CONFIG_ENV_KEY); fileEnv == "" {
		workDir, _ := os.Getwd()
        file = workDir + "/config/" + utils.CONFIG_DEF_FILE
    } else {
        file = fileEnv
    }

	fmt.Println("using config file:", file)

    v := viper.New()
    v.SetConfigFile(file)
    v.SetConfigType(utils.CONFIG_FILE_TYPE)

    err := v.ReadInConfig()
    if err != nil {
        panic(fmt.Errorf("Failed to read config: %s \n", err))
    }
    v.WatchConfig()

    v.OnConfigChange(func(e fsnotify.Event) {
        fmt.Println("config file changed:", e.Name)
        if err := v.Unmarshal(conf); err != nil {
            fmt.Println(err)
        }
    })
    if err := v.Unmarshal(conf); err != nil {
        fmt.Println(err)
    }

    return v
}

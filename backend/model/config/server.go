package config

type Server struct {
	Host         string `mapstructure:"host" json:"host" yaml:"host"`                             // port
	Port         int `mapstructure:"port" json:"port" yaml:"port"`                             // port
}

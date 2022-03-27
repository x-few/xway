package config

type Config struct {
	Server Server `mapstructure:"server" json:"server" yaml:"server"`
	Database Database `mapstructure:"database" json:"database" yaml:"database"`
}

package config

type Config struct {
	Server Server `mapstructure:"server" json:"server" yaml:"server"`
	Database Database `mapstructure:"database" json:"database" yaml:"database"`
	IDGenerator IDGenerator `mapstructure:"id-generator" json:"id-generator" yaml:"id-generator"`
}

package config

type IDGenerator struct {
	Type         string `mapstructure:"type" json:"type" yaml:"type"`                             // port
	MachineID    int `mapstructure:"machine-id" json:"machine-id" yaml:"machine-id"`                             // port
}

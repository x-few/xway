package config

type Database struct {
	Type         string `mapstructure:"path" json:"path" yaml:"path"`                             // db type: postgres
	Host         string `mapstructure:"path" json:"path" yaml:"path"`                             // server address:port
	Port         string `mapstructure:"port" json:"port" yaml:"port"`                             // port
	Dbname       string `mapstructure:"db-name" json:"dbname" yaml:"db-name"`                     // database name
	Username     string `mapstructure:"username" json:"username" yaml:"username"`                 // username
	Password     string `mapstructure:"password" json:"password" yaml:"password"`                 // password
	Config       string `mapstructure:"config" json:"config" yaml:"config"`                       // advanced configuration
	MaxIdleConns int    `mapstructure:"max-idle-conns" json:"maxIdleConns" yaml:"max-idle-conns"` // max idle connections
	MaxOpenConns int    `mapstructure:"max-open-conns" json:"maxOpenConns" yaml:"max-open-conns"` // max open connections
}

func (p *Database) Dsn() string {
	return "host=" + p.Host + " user=" + p.Username + " password=" + p.Password + " dbname=" + p.Dbname + " port=" + p.Port + " " + p.Config
}


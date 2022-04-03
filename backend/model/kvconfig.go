package model

type KVConfigs struct {
	ID          uint64         `json:"id" gorm:"primarykey"`
	Key         string         `json:"key" gorm:"unique;not null;comment:key"`
	Value       string         `json:"value" gorm:"comment:value"`
	DateTime
}

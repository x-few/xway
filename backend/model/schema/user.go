package schema

import (
	"github.com/x-few/xway/backend/model"
)

type Users struct {
	ID          uint64         `json:"id" gorm:"primarykey"`
	Username    string         `json:"username" gorm:"unique;not null;comment:username"`
	Password    string         `json:"-" gorm:"comment:password, hashed"`
	Status      int            `json:"status" gorm:"comment:1:enabled 2:disabled"`
	Creator     uint64         `json:"creator" gorm:"comment:who create this user"`
	Phone       string         `json:"phone" gorm:"comment:phone"`
	Email       string         `json:"email" gorm:"comment:email"`
    model.DateTime
}

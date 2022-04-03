package model

import (
	"time"

	"gorm.io/gorm"
)

type DateTime struct {
	CreatedAt time.Time		`json:"created_at" gorm:"comment:created at"`
	UpdatedAt time.Time		`json:"updated_at" gorm:"comment:updated at"`
}

type DateTimeWithDelete struct {
	DateTime
	DeletedAt gorm.DeletedAt 	`json:"-" gorm:"index"`
}


package initialize

import (
	"os"
	"time"
	"errors"
	"strconv"

	"github.com/sony/sonyflake"

	"github.com/x-few/xway/backend/global"
	"github.com/x-few/xway/backend/utils/constant"
)

func getMachineID() (uint16, error) {
	var machineID uint16

    if tmp := os.Getenv(constant.ENV_SF_MACHINE_ID_KEY); tmp != "" {
		tmp64, err := strconv.ParseUint(tmp, 10, 16)
		if err != nil {
			return 0, err
		}

		machineID = uint16(tmp64)
    } else {
		machineID = uint16(global.CONFIG.IDGenerator.MachineID)
    }

	return machineID, nil
}


func Snowflake() error {
	var st sonyflake.Settings

	st.MachineID = getMachineID
	st.StartTime = time.Date(2022, 4, 1, 0, 0, 0, 0, time.UTC)

	global.SF = sonyflake.NewSonyflake(st)
	if global.SF == nil {
		return errors.New("sonyflake not created")
	}

	return nil
}

package response

type Login struct {
	Token     string         `json:"token"`
	Type      string         `json:"type"`
}

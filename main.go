package main

import (
	"fmt"
	"log"
	"os"

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Create a new app
	myApp := app.New()
	myWindow := myApp.NewWindow("Logging Service")

	// Set up the log file
	file, err := os.OpenFile("logs.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	logger := log.New(file, "", log.LstdFlags)

	// Set up UI elements
	logArea := widget.NewMultiLineEntry()
	logArea.SetPlaceHolder("Log output will appear here...")
	logArea.SetReadOnly(true)

	messageEntry := widget.NewEntry()
	messageEntry.SetPlaceHolder("Enter your log message...")

	logLevel := widget.NewSelect([]string{"INFO", "WARNING", "ERROR"}, func(value string) {
		fmt.Println("Selected log level:", value)
	})

	logButton := widget.NewButton("Log Message", func() {
		msg := messageEntry.Text
		level := logLevel.Selected
		if level == "" {
			level = "INFO"
		}
		formattedMsg := fmt.Sprintf("[%s] %s", level, msg)
		logArea.SetText(logArea.Text + formattedMsg + "\n")

		switch level {
		case "INFO":
			logger.Println("INFO:", msg)
		case "WARNING":
			logger.Println("WARNING:", msg)
		case "ERROR":
			logger.Println("ERROR:", msg)
		default:
			logger.Println("INFO:", msg)
		}
	})

	// Set up the layout
	content := container.NewVBox(
		logArea,
		messageEntry,
		logLevel,
		logButton,
	)

	myWindow.SetContent(content)
	myWindow.Resize(fyne.NewSize(400, 400))
	myWindow.ShowAndRun()
}

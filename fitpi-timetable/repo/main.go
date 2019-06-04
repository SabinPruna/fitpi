package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"sort"
	"strconv"
	"strings"
	"timetable"
)


func GetCourses() []Course {
	unmerged, _ := xlsx.FileToSliceUnmerged("Orar_sem_II_2018-2019_V4.xlsx")
	content := unmerged[0]

	courses := []Course{}

	for index, row := range content {
		if (row[0] != "1" && row[0] != "2" && row[0] != "3") || row[1] == "Codul Orarului: " {
			continue
		}

		year := row[0]
		spec := row[1]
		group := row[2]
		semi := row[3]

		for i := 4; i < len(row); i++ {
			name, courseType, location, teacher := parseCourseCell(row[i])

			if name != "" {
				courses = append(courses, Course{
					Day:            getDay(i),
					Group:          group,
					Hours:          getHours(i),
					Location:       location,
					Name:           name,
					SemiGroup:      semi,
					Specialisation: spec,
					Teacher:        teacher,
					Type:           courseType,
					WeekType:       getWeekType(index),
					Year:           year})
			}
		}
	}

	return courses
}

func search(courses []Course, day time.Weekday, discipline string, location string, year string, spec string, teacher string, courseType string, semi string) []Course {
	return []Course{}
}

//----------------------------------PRIVATES--------------------------------------------

func getWeekType(index int) string {
	if index%2 == 0 {
		return "Even"
	}

	return "Odd"
}

func getHours(index int) string {

	dayIndex := (index - 4) % 7

	switch dayIndex {
	case 0:
		return "8,00-9,50"
	case 1:
		return "10,00-11,50"
	case 2:
		return "12,00-13,50"
	case 3:
		return "14,00-15,50"
	case 4:
		return "16,00-17,50"
	case 5:
		return "18,00-19,50"
	case 6:
		return "20,00-21,50"
	}

	return "Unknown"
}

func getDay(index int) time.Weekday {
	switch {
	case index >= 4 && index <= 10:
		return time.Monday
	case index >= 11 && index <= 17:
		return time.Tuesday
	case index >= 18 && index <= 24:
		return time.Wednesday
	case index >= 25 && index <= 31:
		return time.Thursday
	case index >= 32 && index <= 38:
		return time.Thursday
	default:
		return time.Sunday
	}
}

func parseCourseCell(row string) (string, string, string, string) {
	if row == "" {
		return "", "", "", ""
	}
	splitted := strings.Split(row, ",")

	if len(splitted) != 4 {
		return "", "", "", ""
	}

	return splitted[0], splitted[1], splitted[2], splitted[3]
}


var courses []timetable.Course

func main() {

	//6.78
	//concurrency.SequentialWordCount()

	//5.25
	//concurrency.ParallelWordCount()

	//koch.MakePng()

	http.Handle("/", http.FileServer(http.Dir("./static")))

	http.HandleFunc("/timetable", timetableHandler)

	fmt.Printf("Starting server...\n")
	if err := http.ListenAndServe(":8990", nil); err != nil {
		log.Fatal(err)
	}
}

func timetableHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/timetable" {
		http.Error(w, "404 not found.", http.StatusNotFound)
		return
	}

	switch r.Method {
	case "GET":
		nr, _ := strconv.Atoi(r.URL.Query().Get("Hour")) //["Hour"][0]
		event := MyEvent{OneOrAll: r.URL.Query()["OneOrAll"][0],
			Day:  r.URL.Query()["Day"][0],
			Hour: nr}

		courses = timetable.GetCourses()

		myCourses := []timetable.Course{}
		myCourses = timetable.Search(courses, "*", "Monday", "*", "3", "I", "*", "10LF 262", "A", "*")
		myCourses = append(myCourses, timetable.Search(courses, "*", "Tuesday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Wednesday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Thursday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Friday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Saturday", "*", "3", "I", "*", "10LF 262", "A", "*")...)

		oddCourses := []timetable.Course{}

		for _, course := range myCourses {
			if course.WeekType == "Odd" {
				oddCourses = append(oddCourses, course)
			}
		}

		if event.OneOrAll == "All" {
			str, _ := json.Marshal(courses)
			w.Header().Set("Content-Type", "application/json")
			w.Write(str)
		} else {
			day := event.Day
			if day == "Saturday" || day == "Sunday" {
				day = "Monday"
			}

			dayCourses := []timetable.Course{}

			for _, course := range oddCourses {
				if timetable.ToStringWeekday(course.Day) == day {
					dayCourses = append(dayCourses, course)
				}
			}

			hour := event.Hour
			if event.Hour < 8 || event.Hour > 22 {
				hour = 8
			}

			hourString := strconv.Itoa(hour)

			sort.Slice(dayCourses, func(i, j int) bool {
				return dayCourses[i].Hours < dayCourses[j].Hours
			})

			c, ok := dayCourses[0], false
			for _, course := range dayCourses {
				if strings.Contains(course.Hours, hourString) {
					c = course
					ok = true
					break
				}
			}

			if ok {
				crs, _ := json.Marshal(c)
				w.Header().Set("Content-Type", "application/json")
				w.Write(crs)
			} else {
				newDay := timetable.ToStringWeekday(dayCourses[0].Day + 1)
				newCourses := timetable.Search(courses, "*", newDay, "*", "3", "I", "*", "10LF 262", "A", "*")
				sort.Slice(newCourses, func(i, j int) bool {
					return newCourses[i].Hours < newCourses[j].Hours
				})
				c, _ := json.Marshal(newCourses[0])

				w.Header().Set("Content-Type", "application/json")
				w.Write(c)
			}
		}

		// courses = timetable.GetCourses()
		// searchTemplate := timetable.GetSearchTemplate(courses)
		// timetableTemplate := template.Must(template.ParseFiles("static/timetableForm.html"))

		// timetableTemplate.Execute(w, searchTemplate)

		//http.ServeFile(w, r, "static/timetable.html")
	case "POST":
		// Call ParseForm() to parse the raw query and update r.PostForm and r.Form.
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "ParseForm() err: %v", err)
			return
		}

		// teacher := r.FormValue("teacher")
		// day := r.FormValue("day")
		// discipline := r.FormValue("discipline")
		// year := r.FormValue("year")
		// specialisation := r.FormValue("specialisation")
		// courseType := r.FormValue("courseType")
		// group := r.FormValue("group")
		// semiGroup := r.FormValue("semiGroup")
		// hours := r.FormValue("hours")

		courses = timetable.GetCourses()

		myCourses := []timetable.Course{}
		myCourses = timetable.Search(courses, "*", "Monday", "*", "3", "I", "*", "10LF 262", "A", "*")
		myCourses = append(myCourses, timetable.Search(courses, "*", "Tuesday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Wednesday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Thursday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Friday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
		myCourses = append(myCourses, timetable.Search(courses, "*", "Saturday", "*", "3", "I", "*", "10LF 262", "A", "*")...)

		oddCourses := []timetable.Course{}

		for _, course := range myCourses {
			if course.WeekType == "Odd" {
				oddCourses = append(oddCourses, course)
			}
		}

		if "One" == "All" {
			str, err := json.Marshal(courses)
			println(string(str), err)
		} else {
			day := "Sunday"
			if day == "Saturday" || day == "Sunday" {
				day = "Monday"
			}

			dayCourses := []timetable.Course{}

			for _, course := range oddCourses {
				if timetable.ToStringWeekday(course.Day) == day {
					dayCourses = append(dayCourses, course)
				}
			}

			hour := 9
			if hour < 8 || hour > 22 {
				hour = 8
			}

			hourString := strconv.Itoa(hour)

			sort.Slice(dayCourses, func(i, j int) bool {
				return dayCourses[i].Hours < dayCourses[j].Hours
			})

			c, ok := dayCourses[0], false
			for _, course := range dayCourses {
				if strings.Contains(course.Hours, hourString) {
					c = course
					ok = true
					break
				}
			}

			if ok {
				crs, err := json.Marshal(c)
				println(string(crs), err)
			} else {
				newDay := timetable.ToStringWeekday(dayCourses[0].Day + 1)
				newCourses := timetable.Search(courses, "*", newDay, "*", "3", "I", "*", "10LF 262", "A", "*")
				sort.Slice(newCourses, func(i, j int) bool {
					return newCourses[i].Hours < newCourses[j].Hours
				})
				c, err := json.Marshal(newCourses[0])

				println(string(c), err)
			}
		}
		returnedJSON, _ := json.Marshal(oddCourses)

		println(string(returnedJSON))

		//timetableTemplate := template.Must(template.ParseFiles("static/timetableForm.html"))

		//timetableTemplate.Execute(w, searchTemplate)

	default:
		fmt.Fprintf(w, "Sorry, only GET and POST methods are supported.")
	}
}

//MyEvent used to identify wether it should send all things or only closest
type MyEvent struct {
	OneOrAll string `json:"OneorAll"`
	Day      string `json:"Day"`
	Hour     int    `json:Hour`
}

//HandleRequest used in lambda function
func HandleRequest(ctx context.Context, event MyEvent) (string, error) {
	courses = timetable.GetCourses()

	myCourses := []timetable.Course{}
	myCourses = timetable.Search(courses, "*", "Monday", "*", "3", "I", "*", "10LF 262", "A", "*")
	myCourses = append(myCourses, timetable.Search(courses, "*", "Tuesday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
	myCourses = append(myCourses, timetable.Search(courses, "*", "Wednesday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
	myCourses = append(myCourses, timetable.Search(courses, "*", "Thursday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
	myCourses = append(myCourses, timetable.Search(courses, "*", "Friday", "*", "3", "I", "*", "10LF 262", "A", "*")...)
	myCourses = append(myCourses, timetable.Search(courses, "*", "Saturday", "*", "3", "I", "*", "10LF 262", "A", "*")...)

	oddCourses := []timetable.Course{}

	for _, course := range myCourses {
		if course.WeekType == "Odd" {
			oddCourses = append(oddCourses, course)
		}
	}

	if event.OneOrAll == "All" {
		str, err := json.Marshal(courses)
		return string(str), err
	} else {
		day := event.Day
		if day == "Saturday" || day == "Sunday" {
			day = "Monday"
		}

		dayCourses := []timetable.Course{}

		for _, course := range oddCourses {
			if timetable.ToStringWeekday(course.Day) == day {
				dayCourses = append(dayCourses, course)
			}
		}

		hour := event.Hour
		if event.Hour < 8 || event.Hour > 22 {
			hour = 8
		}

		hourString := strconv.Itoa(hour)

		sort.Slice(dayCourses, func(i, j int) bool {
			return dayCourses[i].Hours < dayCourses[j].Hours
		})

		c, ok := dayCourses[0], false
		for _, course := range dayCourses {
			if strings.Contains(course.Hours, hourString) {
				c = course
				ok = true
				break
			}
		}

		if ok {
			crs, err := json.Marshal(c)
			return string(crs), err
		} else {
			newDay := timetable.ToStringWeekday(dayCourses[0].Day + 1)
			newCourses := timetable.Search(courses, "*", newDay, "*", "3", "I", "*", "10LF 262", "A", "*")
			sort.Slice(newCourses, func(i, j int) bool {
				return newCourses[i].Hours < newCourses[j].Hours
			})
			c, err := json.Marshal(newCourses[0])

			return string(c), err
		}
	}

	return "None", errors.New("None")
}

// func main() {
// 	lambda.Start(HandleRequest)
// }

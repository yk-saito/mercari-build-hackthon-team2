package models

import (
	"database/sql"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

type Items struct {
	Items []Item `json:"items"`
}

type Item struct {
	Id       int    `json:"id"`
	Name     string `json:"name"`
	Category string `json:"category"`
	Image    string `json:"image_filename"`
}

func GetItem(db *sql.DB, query string) ([]Item, error) {
	if query == "" {
		query = "SELECT * FROM items"
	}

	stmt, err := db.Prepare(query)
	if err != nil {
		return nil, err
	}

	defer stmt.Close()

	rows, err := stmt.Query()
	if err != nil {
		return nil, err
	}

	items := make([]Item, 0)
	for rows.Next() {
		var item Item
		if err := rows.Scan(&item.Id, &item.Name, &item.Category, &item.Image); err != nil {
			return nil, err
		}
		items = append(items, item)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return items, err
}

func GetItemById(db *sql.DB, id string) (Item, error) {
	item := Item{}

	stmt, err := db.Prepare("SELECT items.name, items.category, items.image_filename FROM items WHERE items.id = ?")
	if err != nil {
		return item, err
	}

	sqlErr := stmt.QueryRow(id).Scan(&item.Name, &item.Category, &item.Image)
	switch {
	case sqlErr == sql.ErrNoRows:
		return item, fmt.Errorf("No item with id %s", id)
	case sqlErr != nil:
		return item, sqlErr
	default:
		return item, nil
	}
}

func AddItem(db *sql.DB, newItem Item) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}

	// Save data
	stmt, err := tx.Prepare("INSERT INTO items(name, category, image_filename) VALUES(?, ?, ?)")
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.Exec(newItem.Name, newItem.Category, newItem.Image)
	if err != nil {
		return err
	}

	if err := tx.Commit(); err != nil {
		return err
	}

	return nil
}

func SearchItem(db *sql.DB, key string) ([]Item, error) {
	q := fmt.Sprintf("SELECT items.name, items.category, items.image_filename FROM items WHERE items.name = '%s' or items.category = '%s'",
		key, key)

	items, err := GetItem(db, q)

	return items, err
}

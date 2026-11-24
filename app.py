
            values.append(record_id)

            conn = get_db_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        f"UPDATE {item['table']} "
                        f"SET {', '.join(assignments)} "
                        f"WHERE {item['pk']} = %s",
                        values
                    )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()

            flash(
                f"{item['title']} record updated successfully.",
                "success"
            )

            return redirect(
                url_for("list_records", key=key)
            )

        return render_template(
            "form.html",
            item=item,
            key=key,
            record=record,
            mode="Edit"
        )

    except (ValueError, Error) as exc:
        flash(str(exc), "danger")

        return render_template(
            "form.html",
            item=item,
            key=key,
            record=record,
            mode="Edit"
        )


@app.post("/<key>/<int:record_id>/delete")
def delete_record(key, record_id):
    item = get_table(key)
    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cur:
            cur.execute(
                f"DELETE FROM {item['table']} "
                f"WHERE {item['pk']} = %s",
                (record_id,)
            )

            deleted = cur.rowcount

        conn.commit()

        flash(
            "Record deleted." if deleted
            else "Record was not found.",
            "success"
        )

    except IntegrityError:
        if conn:
            conn.rollback()

        flash(
            "This record is referenced by another table. "
            "Remove or update dependent records first.",
            "danger"
        )

    except Error as exc:
        if conn:
            conn.rollback()

        app.logger.exception("Delete operation failed")

        flash(f"Database error: {exc}", "danger")

    finally:
        if conn:
            conn.close()

    return redirect(
        url_for("list_records", key=key)
    )


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5000")),
        debug=True
    )

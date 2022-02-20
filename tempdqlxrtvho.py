ption as e:
            keep.clear_note(movie_link_note_id)
            error_log = keep.edit_note(error_log_id, e)
            print(e)
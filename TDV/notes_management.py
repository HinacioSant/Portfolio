from .models import notes

class notes_management: # Overall management.
    def __init__(self, form, user):
        self.form = form
        self.user = user

    def bullet_management(self): # Bullet management.
        type = "bullet" # Add "type" variable.

        try: # Check if is a delete request for a bullet.
            if self.form['del_b']: # If it is
                bullet_object = notes.objects.filter(user=self.user, type=type, finished=True) # Query the object.
                bullet_object.delete() # And delete it.
                response = "redirect_notes" # Return reditect to notes page.

                return response
        except KeyError:
            pass

        # If not a delete request then is a update finish status request
        for a in self.form: # Loop because of multiple objects
            # Don't add to the loop empty objects and the csrf token.
            if a != 'csrfmiddlewaretoken' and self.form[a] != '': # If neither only valid bullet objects on the loop.
                bullet_object = notes.objects.filter(user=self.user, type=type, id= a) # query those objects.
                # "a" = the id of the object and the value is the action.
                if self.form[a] == "off": # If action "off"
                    bullet_object.update(finished=False) # Update.

                elif self.form[a] == "on": # If action "on"
                    bullet_object.update(finished=True) # Update.

                # Check notes_page.html for more info.

    def notes_add(self): # management of notes and add of bulltes
        try: # Check if is a delete request for a note.
            if self.form['del_n']: # If it is
                note_object = notes.objects.get(user=self.user, type="note", id=self.form['del_n'])# Query the object.
                note_object.delete() # And delete it.
                response = "redirect_notes" # Return reditect to notes page.

                return response
        except KeyError:
            pass

        try:
            if self.form['type'] == 'note': # Check for respective type.
                # Then add them.                

                add = notes(user=self.user, title=self.form['title'], subject=self.form['subject'], type=self.form['type'], content=self.form['content'], finished=False)
                add.save()

                response = "redirect_notes" # Return reditect to notes page.

                return response
        except KeyError:
            pass

        try:
            if self.form['type'] == 'bullet': # Check for respective type.
                # Then add them.
                if self.form['title'] == "" or self.form['subject'] == "":
                    return "redirect_notes"

                add = notes(user=self.user, title=self.form['title'], subject=self.form['subject'], type=self.form['type'], finished=False)
                add.save()
                response = "redirect_notes" # Return reditect to notes page.

                return response
        except KeyError:
            pass

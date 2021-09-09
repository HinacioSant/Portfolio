from .models import notes

class notes_management:
    def __init__(self, form, user):
        self.form = form
        self.user = user

    def bullet_management(self):
        type = "bullet"

        try:
            if self.form['del_b']:
                bullet_object = notes.objects.filter(user=self.user, type=type, finished=True)
                bullet_object.delete()
                response = "redirect_notes"

                return response
        except KeyError:
            pass

        for a in self.form:
            if a != 'csrfmiddlewaretoken' and self.form[a] != '':
                bullet_object = notes.objects.filter(user=self.user, type=type, id= a)

                if self.form[a] == "off":
                    bullet_object.update(finished=False)

                elif self.form[a] == "on":
                    bullet_object.update(finished=True)


    def notes_add(self):
        try:
            if self.form['del_n']:
                note_object = notes.objects.get(user=self.user, type="note", id=self.form['del_n'])
                note_object.delete()
                response = "redirect_notes"

                return response
        except KeyError:
            pass

        try:
            if self.form['type'] == 'note':
                add = notes(user=self.user, title=self.form['title'], subject=self.form['subject'], type=self.form['type'], content=self.form['content'], finished=False)
                add.save()                
        except KeyError:
            pass

        try:
            if self.form['type'] == 'bullet':
                add = notes(user=self.user, title=self.form['title'], subject=self.form['subject'], type=self.form['type'], finished=False)
                add.save()
                response = "redirect_notes"

                return response
        except KeyError:
            pass

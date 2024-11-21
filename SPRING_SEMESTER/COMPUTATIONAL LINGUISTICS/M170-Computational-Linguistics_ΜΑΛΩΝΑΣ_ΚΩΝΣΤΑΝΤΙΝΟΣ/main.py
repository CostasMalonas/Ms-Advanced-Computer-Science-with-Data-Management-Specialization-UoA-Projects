import MouseController as ms

# Φωνητικές Εντολές:
# 1) πάνω - κάτω - αριστερά - δεξιά αριθμός π.χ (δεξιά 100)
#     Ο mouse cursor θα μετακινηθεί 100 pixel δεξιά
# 2) νέα αναζήτηση 
#     Θα πούμε το καινούργιο search term αφού πρώτα το πρόγραμμα μας πεί "Please say your search term"
# 3) click - κλίκ (same thing :D)
#     Για το mouse click functionality
# 4) Όταν το mouse cursor είναι π.χ πάνω από κάποιο search bar και πούμε click και εφανιστεί το cursor
#    που υποδικνύει ότι αναμένετε είσοδος από το keyboard, ο χρήστης μπορεί να πεί type και αφού ακουστεί το "Please say what you want to type"
#    ο χρήστης λέει αυτό που θέλει να πληκτρολογήσει και πατιέται αυτόματα ENTER αλλιώς μπορεί να πεί delete ή διαγραφή για να διγραφεί 
#    οτιδήποτε υπάρχει στο search bar.
# 5) Πίσω: για να πάμε στην προηγούμενη σελίδα από την οποία ήμασταν 


if __name__ == "__main__":
    controller = ms.MouseController()
    controller.start()
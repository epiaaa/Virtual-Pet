
def gain_experience(pet_model, experience):
    pet_model.experience += experience


def upgrade(pet_model):
    if pet_model.experience >= upgrade_need_experience(pet_model.level):
        pet_model.level += 1
        pet_model.save_Pet_infos()
        # print("Pet model upgraded to version 2")


def upgrade_need_experience(lever):
    if lever < 10:
        need_experience = 200+100*lever
    elif lever < 50:
        need_experience = 200+pow((10*lever), 1.5)
    else:
        need_experience = 11400*pow(1.1, lever-50)
    return need_experience

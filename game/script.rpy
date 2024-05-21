init python:
    from gameplay import Army, Game, Squad, Battlefield
    import random

```Screens```

screen hq_screen:
    frame:
        xpos 1100
        vbox:
            text "Номер хода:[game_main.turn_number]"
            text "Пехота:[wagner_army.troops]"
            text "Техника:[wagner_army.vehicles]"
            text "Танки:[wagner_army.tanks]"
            text "Артиллерия:[wagner_army.artillery]"
            text "Откат до вербовки: [game_main.cooldown_recruit]"
            text "Откат до битвы: [game_main.cooldown_battle]"
            text "Контроль над городом: [game_main.control_city]"
            textbutton "Рекрутирование" action Function(game_main.recruit_troop)
            textbutton "Следующий ход" action Function(game_main.next_turn, battlefield_bakhmut)
            textbutton "Одержать победу ЧИТ" action SetVariable('game_main.control_city', 100)
            if game_main.control_city >= 100:
                textbutton "Обьявить о победе!" action (Jump("GameEnd"), Hide("hq_screen"))

    
    frame:
        xpos 200
        vbox:
            textbutton "Тактическа карта" action (Jump('TacticalMap'), Hide("hq_screen"))
            textbutton "Список отрядов" action (Jump('SquadList'), Hide("hq_screen"))
            textbutton "Создать отряд" action (Jump('SquadCreate'), Hide("hq_screen"))


screen squad_table:
    frame:
        xpos 10
        vpgrid:
            cols 4
            spacing 30
            xsize 1700
            ysize 1600

            scrollbars "vertical"
            mousewheel True
            for squad_name in game_main.squad_dict:
                vbox:
                    textbutton "{}".format(squad_name) action (SetVariable("squad_info_key", squad_name), Jump("SquadInfoPanel"))

    frame:
        xpos 1780
        vbox:
            textbutton "Назад" action Jump("bakhmut")


screen InfoPanel:
        frame:
            vbox:
                text "Имя отряда:[game_main.squad_dict[squad_info_key].name]"
                text "Пехота:[game_main.squad_dict[squad_info_key].troop]"
                text "Техника:[game_main.squad_dict[squad_info_key].vehicle]"
                text "Танки:[game_main.squad_dict[squad_info_key].tank]"
                text "Сила отряда:[game_main.squad_dict[squad_info_key].squad_power()]"
                textbutton "Назад" action Jump("bakhmut")
                if game_main.order_status is True:
                    textbutton "Выбрать этот отряд" action (Function(battlefield_bakhmut.points[active_battle_point].place_wagner_squad, game_main.squad_dict[squad_info_key]),
                                                            Function(game_main.end_order_to_squad),
                                                            Function(game_main.send_squad, game_main.squad_dict[squad_info_key].name),
                                                            Jump("TacticalMap"))


screen create_squad_screen:
        default squadtroop = 0
        default squadvehicle = 0
        default squadtank = 0
        frame:
            vbox:
                spacing 20

                text "Имя отряда:[squadname]"
                text "Пехота:[squadtroop]"
                bar value ScreenVariableValue("squadtroop", 100) style "slider"
                text "Техника:[squadvehicle]"
                bar value ScreenVariableValue("squadvehicle", 15) style "slider"
                text "Танки:[squadtank]"
                bar value ScreenVariableValue("squadtank", 4) style "slider"
                textbutton "Создать отряд" action (Function(game_main.squad_add, Squad(squadname, squadtroop, squadvehicle, squadtank, 1)),
                                                            Jump("bakhmut"))

            vbox:
                ypos 800
                text "Если вы не добавите ни одной единицы, отряд не будет создан.\n\nДопускается создание отрядов с одинаковыми названиями."


screen tactical_panel:
        frame:
            vbox:
                for battle_point_name in battlefield_bakhmut.points.keys():
                    textbutton "{}".format(battle_point_name) action (SetVariable("active_battle_point", battle_point_name), Jump("PointInteraction"))


screen battle_point:
    python:
        use_point = battlefield_bakhmut.points[active_battle_point]
        enemy_squad = use_point.enemy_squad
        wagner_squad = use_point.wagner_squad
        wagner_status = use_point.empty_squad_check()

    frame:
        vbox:
            if use_point.clear_status is True:
                text "[use_point.name]"
                text "[enemy_squad.name]"
                text"Статус: Зачищено"
            else:
                text "[use_point.name]"
                text "[enemy_squad.name]"
                text "Пехота:[enemy_squad.troop]"
                text "Техника:[enemy_squad.vehicle]"
                text "Танк:[enemy_squad.tank]"
                text"Статус: Контролируется противником"

            if use_point.clear_status is False and enemy_squad.name != "No Squad" and wagner_squad.name == "No Squad":
                textbutton "Назначить отряд" action (Function(game_main.order_to_squad), Jump("SquadList"))
                textbutton "Завершить миссию ЧИТ" action Function(use_point.clear_point)
                textbutton "Назад" action Jump("bakhmut")
            elif use_point.clear_status is False and enemy_squad.name != "No Squad" and wagner_squad.name != "No Squad":
                textbutton "Атаковать" action (Function(use_point.battle_on_point),
                                                Function(game_main.return_squad, wagner_squad), 
                                                Jump("bakhmut"))
                textbutton "Отступить" action (Function(use_point.fallback_squad), 
                                                Function(game_main.return_squad, wagner_squad))
            else:
                textbutton "Назад" action Jump("bakhmut")


```Labels```


label start:
    default wagner_army = Army('Wagner Group', 20000, 120, 32, 12, 120)
    default hohol_army = Army('Nazi Group', 40000, 135, 32, 44, 500)
    default game_main = Game(wagner_army, hohol_army, {}, 1, 10, 10, 50)
    default used_wagner_squad = ''
    default active_squad = "No Squad"
    default active_battle_point = ''
    default squad_info_key = ''
    default battlefield_bakhmut = Battlefield({})
    default control_city = game_main.control_city
    "Добро пожаловать в Бахмут"
    jump bakhmut


label bakhmut:
    call screen hq_screen


label SquadList:
    if len(game_main.squad_dict) is 0:
        "Нет подготовленных отрядов"
        jump bakhmut
    else:
        call screen squad_table

    call screen squad_info


label SquadInfoPanel:

    call screen InfoPanel


label SquadCreate:

    python:
        squadname = renpy.input("введите имя отряда")
        squadname = squadname.strip() or "Отряд {}".format(random.randrange(1, 100))


    call screen create_squad_screen


label TacticalMap:

    if len(battlefield_bakhmut.points) != 0:
        call screen tactical_panel
    else:
        "Нет точек контакта"
        jump bakhmut


label PointInteraction:

    python:
        use_point = battlefield_bakhmut.points[active_battle_point]
        wagner_status = use_point.empty_squad_check()
    
    call screen battle_point


label GameEnd:
    "Вагнер победил"
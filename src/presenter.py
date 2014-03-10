# 'presenter.py' in 'tasks-cmd-line-sample'
#   '2/15/14'/'9:33 AM'
#     Presenter: intermediary, middle man
#         modules:
# import task_model
#           presenter_class.py, task_class.py
#         typically handling user events
#             ?? what are my events ??
#           update() is probably the most important and basic one.
#             !! user request for different views:
#                 ThisWeek, Today, FacetsSummary, etc
#             !! or time generated - daily - reports
#         business logic
#             presenter.update()


# def update():
    # view event calls update
    # call model.update()
    #   which
    #       gets tasks from server
    #       validates properties
    #       creates taskclass instances
    #       applies taskclass rules
    #       patches updated tasks to server
    # builds a series of output lists for Views
    # pass




import view.mainView.mainView as MainView
import view.mashCompareView.mashCompareView as MashCompare
import app.services.mashFileServices.mashFileService as table
import app.repositories.mashFileRepository.mashFileRepository as repo
mainView = MainView.MainView()
mashCompareView = MashCompare.MashCompare()
view = 'main view'
#'Z:\cad\TDMPT306_R00\TDMPT3U6_R00_mash_04.xls'

test = table.MashFileService(repo.MashFileRepository())
for i in range(25):
    print((test.get_mash_table('Z:\cad\TDMPT306_R00\TDMPT3U6_R00_mash_04.xls'))[i])

while view:
    if view == 'main view':
        mainView.run_window()
        view = mainView.view
    elif view == 'Compare Mash':
        mashCompareView.run_window()
        view = mashCompareView.view


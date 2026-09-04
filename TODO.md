# TODO: migracja GUI z CustomTkinter do PySide6

## Cel refaktoryzacji

Przenieść warstwę GUI do PySide6 bez zmieniania logiki biznesowej w trakcie
migracji. Po każdym etapie aplikacja powinna się uruchamiać, a przeniesiony
przepływ powinien działać od kliknięcia przycisku aż do pokazania wyniku.

Pliki referencyjne:

- `project/GUI/main_windows.py.bak` — zachowanie starego okna głównego,
- `project/GUI/popups.py.bak` — zachowanie starych popupów,
- `project/core/controllers.py` — kontrakt, który nowy widok musi obsłużyć.

Nie należy jeszcze usuwać plików `.bak`. Są specyfikacją zachowania starego GUI.

## Zasady pracy

- [ ] Migrować jedną funkcję aplikacji naraz, razem z jej popupem i widokiem wyniku.
- [ ] Nie zmieniać jednocześnie GUI i obliczeń w `controllers.py`.
- [ ] Zachować nazwy metod wywoływanych przez kontroler albo świadomie zmienić
      kontroler i widok w tym samym kroku.
- [ ] Po każdym etapie uruchomić aplikację i ręcznie sprawdzić ukończony przepływ.
- [ ] Po każdym działającym etapie zrobić osobny commit.
- [ ] Nie używać `tkinter`, `customtkinter`, `.root`, `.after()`, `.pack()` ani
      `.grid()` w kodzie przeniesionym do PySide6.
- [ ] Wszystkie zmiany widżetów wykonywane z wątku roboczego przekazywać do
      głównego wątku przez sygnały Qt.

## Etap 0 — zabezpieczenie kontraktu widoku

Obecny kontroler wywołuje poniższe metody. Traktuj tę listę jako kontrakt
`MainWindow` i odznaczaj po zaimplementowaniu:

- [x] `show_error(title, message)`
- [x] `show_warning(title, message)`
- [x] `show_yes_no(title, message)`
- [x] `ask_for_file_path(title)`
- [x] `show_schedule_popup(on_confirm)`
- [ ] `show_machine_select_popup(machines, df_mc, on_confirm)`
- [ ] `show_report_params_popup(machines, on_confirm)`
- [ ] `clear_report_view()`
- [ ] `set_print_button_visibility(visible)`
- [ ] `render_sap_report_table(linia, day, rows, user)`
- [ ] `render_db_report_cards(report_text)`
- [ ] `ask_order_id_popup()`
- [ ] `ask_calc_mode_popup(workplace, default_speed, default_pieces_per_shift)`
- [ ] `render_order_confirmation_card(data)`
- [ ] `show_progress_popup(title)`
- [ ] `update_progress_popup(percentage, message)`
- [ ] `show_completion_in_popup(message)`
- [ ] `hide_progress_popup()`

Do czasu implementacji można dodać tymczasowe metody pokazujące komunikat
„Funkcja jest jeszcze w trakcie migracji”. Dzięki temu kliknięcie nie zakończy się
`AttributeError`, a brak funkcji będzie jednoznaczny.

## Etap 1 — szkielet głównego okna

- [ ] Dodać kontener na aktualny raport, np. `self.report_container` z
      `QVBoxLayout`.
- [ ] Napisać `clear_report_view()`, które usuwa widżety z layoutu za pomocą
      `takeAt()` i `deleteLater()`, a następnie pokazuje ekran powitalny.
- [ ] Dodać dolny panel akcji z przyciskami:
  - [ ] Edytuj raport,
  - [ ] Drukuj raport,
  - [ ] Wyślij zapotrzebowanie na folię.
- [ ] Dodać sygnały dla tych trzech przycisków.
- [ ] Podłączyć sygnały w `app.py` do:
  - [ ] `controller.handle_edit_report`,
  - [ ] `controller.handle_print_report`,
  - [ ] `controller.handle_export_foil_report`.
- [ ] Zaimplementować `set_print_button_visibility()` zgodnie z zachowaniem
      starego GUI.
- [ ] Sprawdzić, czy `show_welcome_screen()` i `hide_welcome_screen()` nie
      pozostawiają pustych lub zdublowanych widżetów.

Test etapu:

- aplikacja startuje,
- „Wyczyść” nie zgłasza wyjątku,
- panel akcji można pokazać i ukryć,
- ekran powitalny wraca po wyczyszczeniu.

## Etap 2 — przepływ „Wczytaj maszyny”

### Popup

- [ ] Przenieść `MachineSelectPopup` z `popups.py.bak` jako `QDialog`.
- [ ] Użyć `QScrollArea` lub `QTableWidget` do listy maszyn.
- [ ] Dla każdego wiersza zachować:
  - [ ] wybór maszyny,
  - [ ] wartość sztuk na zmianę,
  - [ ] pracę w sobotę,
  - [ ] pracę w niedzielę.
- [ ] Zachować „Wybierz wszystkie” i „Zapisz terminy”.
- [ ] Walidować, że wybrano co najmniej jedną maszynę i że sztuki/zmianę są
      liczbą większą od zera.
- [ ] Zachować dokładną kolejność argumentów callbacka oczekiwaną przez
      `MainController.on_machines_selected()`.
- [ ] Dodać `MainWindow.show_machine_select_popup(...)`.

### Wynik

- [ ] Przenieść `render_db_report_cards(report_text)` do PySide6.
- [ ] Każdą kartę zbudować z `QFrame`, `QLabel` i layoutów.
- [ ] Cały raport umieścić w `QScrollArea`.
- [ ] Przed renderowaniem wywołać `clear_report_view()` i ukryć ekran powitalny.

Test etapu:

- wybór maszyn działa,
- anulowanie nie uruchamia obliczeń,
- harmonogram zwraca zmianę, tryb startu i datę,
- raport maszyn pojawia się w prawym panelu,
- ponowne uruchomienie funkcji nie dubluje starego raportu.

## Etap 3 — przepływ „Generuj raport”

### Popup parametrów

- [ ] Przenieść `ReportParamsPopup` jako `QDialog`.
- [ ] Użyć `QComboBox` do wyboru maszyny.
- [ ] Użyć `QLineEdit` z `QRegularExpressionValidator` dla numeru zlecenia.
- [ ] Zachować wybór „dziś” / „z daty”.
- [ ] Callback ma zwracać słownik z kluczami:
  - [ ] `linia`,
  - [ ] `start_order_id`,
  - [ ] `day` jako `datetime.date`.
- [ ] Dodać `MainWindow.show_report_params_popup(...)`.

### Tabela raportu

- [ ] Przenieść `render_sap_report_table(...)`.
- [ ] Preferować `QTableWidget` lub model `QTableView` zamiast ręcznego
      tworzenia etykiety dla każdej komórki.
- [ ] Zachować kolumny: LP, INDEKS, ILOŚĆ, JM, SZT.
- [ ] Po wygenerowaniu raportu pokazać właściwe przyciski panelu akcji.

Test etapu:

- wybór pliku można anulować,
- błędne zlecenie pokazuje komunikat,
- tabela wyświetla wszystkie wiersze,
- drukowanie i edycja raportu wywołują metody kontrolera.

## Etap 4 — przepływ „Potwierdź termin”

- [ ] Przenieść `OrderIdPopup` jako `QDialog`.
- [ ] Walidować numer zlecenia jako same cyfry.
- [ ] Zamiast callbacka można zwracać wartość po `exec()`; anulowanie powinno
      zwracać `None`.
- [ ] Zaimplementować `MainWindow.ask_order_id_popup()`.
- [ ] Przenieść `CalcModePopup` jako `QDialog`.
- [ ] Zachować tryby `speed` i `shift` oraz wszystkie klucze zwracanego słownika.
- [ ] Zaimplementować `MainWindow.ask_calc_mode_popup(...)`.
- [ ] Przenieść `render_order_confirmation_card(data)`.

Test etapu:

- anulowanie każdego popupu zatrzymuje przepływ bez błędu,
- błędna data i wartości mniejsze lub równe zero są odrzucane,
- karta końcowa pokazuje maszynę, zlecenie, szczegóły i termin.

## Etap 5 — eksport folii i praca w tle

- [ ] Przenieść `ProgressPopup` jako `QDialog` z `QProgressBar`.
- [ ] Zaimplementować cztery metody obsługi postępu z kontraktu `MainWindow`.
- [ ] Usunąć użycie `self.view.root.after(...)` z
      `project/core/logic/foil_exporter.py`.
- [ ] Wprowadzić obiekt sygnałów Qt, np.:
  - [ ] `progress_changed(int, str)`,
  - [ ] `completed(str)`,
  - [ ] `failed(str)`.
- [ ] Połączyć sygnały z metodami widoku przed uruchomieniem wątku.
- [ ] Nie aktualizować żadnego widżetu bezpośrednio z `threading.Thread`.
- [ ] Wydzielić wybór terminu folii do osobnego `FoilShiftPopup`, zamiast
      pozostawiać go jako metodę `ReportParamsPopup`.
- [ ] Zmienić kontroler tak, aby nie używał `self.view.root`.

Test etapu:

- okno postępu nie zawiesza GUI,
- postęp aktualizuje się podczas pracy,
- sukces i błąd wracają do głównego wątku,
- zamknięcie popupu nie powoduje aktualizacji usuniętego widżetu.

## Etap 6 — Ustawienia, Pomoc i O programie

- [ ] Przenieść `AboutPopup` do PySide6.
- [ ] Przenieść `HelpWindow` do PySide6.
- [ ] Przenieść `ConfigWindow` z CustomTkinter do `QDialog` lub `QMainWindow`.
- [ ] Dla konfiguracji użyć `QTabWidget` i widoków tabel/list.
- [ ] Podłączyć w `app.py` sygnały:
  - [ ] `open_settings_requested`,
  - [ ] `show_help_requested`,
  - [ ] `show_about_requested`.
- [ ] Zdecydować, czy te akcje obsługuje kontroler, czy bezpośrednio
      `MainWindow`; zastosować jeden wariant konsekwentnie.
- [ ] Migrację sprawdzania aktualizacji oprzeć na mechanizmach Qt, np. sygnałach
      i `QTimer`, zamiast `after()`.

Test etapu:

- wszystkie trzy dolne przyciski otwierają dokładnie jedno okno,
- okna mają poprawnego rodzica i modalność,
- zamknięcie okna pomocniczego nie zamyka całej aplikacji.

## Etap 7 — wygląd i motyw

- [ ] Dodać w QSS kolor zwykłych etykiet w dialogach, np. `QDialog QLabel`.
- [ ] Uzupełnić style dla `QComboBox`, `QTableView`/`QTableWidget`,
      `QProgressBar`, `QTabWidget` i pól walidowanych.
- [ ] Zdecydować, czy aplikacja ma mieć przełączanie jasny/ciemny.
- [ ] Jeśli tak, przygotować dwa arkusze QSS lub dwa zestawy zmiennych kolorów.
- [ ] Usunąć style ustawiane bezpośrednio przez `setStyleSheet()` tam, gdzie mogą
      być zastąpione nazwą obiektu i globalnym QSS.

## Etap 8 — testy regresji

- [ ] Dodać test tworzący `QApplication` i `MainWindow` w trybie offscreen.
- [ ] Dodać test sprawdzający, czy `MainWindow` posiada cały kontrakt wymagany
      przez kontroler.
- [ ] Dodać test wyniku `SchedulePopup`.
- [ ] Dodać test walidacji `OrderIdPopup`, `ReportParamsPopup` i
      `CalcModePopup`.
- [ ] Dodać test `clear_report_view()`, aby wykrywać pozostawione widżety.
- [ ] Dodać test sygnałów przycisków bez połączenia z bazą danych.
- [ ] Dla logiki bazy użyć mocków; test GUI nie powinien wymagać VPN ani ODBC.
- [ ] Po każdym etapie uruchamiać co najmniej:

```powershell
python -m compileall -q app.py project assets
```

Po dodaniu pytest-qt:

```powershell
pytest
```

## Etap 9 — zakończenie migracji

Wykonać dopiero, gdy wszystkie wcześniejsze punkty są ukończone:

- [ ] Wyszukać pozostałości `customtkinter`, `tkinter`, `.after(` i `.root`.
- [ ] Upewnić się, że pozostałości dotyczą wyłącznie niezależnych narzędzi, np.
      updatera lub deployera, jeśli nie są częścią migrowanego GUI.
- [ ] Usunąć `customtkinter` z `requirements.txt`, jeżeli nie jest już używany.
- [ ] Usunąć pliki `.bak` dopiero po pełnym teście regresji i zachowaniu ich
      historii w Git.
- [ ] Wykonać ręczny test wszystkich przycisków na czystym uruchomieniu.

## Zalecany podział commitów

1. `refactor(gui): add PySide6 main report container and actions`
2. `refactor(gui): migrate machine selection workflow`
3. `refactor(gui): migrate SAP report workflow`
4. `refactor(gui): migrate order confirmation workflow`
5. `refactor(gui): migrate foil export progress to Qt signals`
6. `refactor(gui): migrate settings help and about windows`
7. `test(gui): add PySide6 regression tests`
8. `chore(gui): remove remaining CustomTkinter dependency`

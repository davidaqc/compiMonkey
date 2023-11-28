from tkinter import messagebox
import tkinter as tk
import pygame
import sys
import os
import math
import semanticAnalysis as ast
import syntacticAnalysis as p
import global_variable
from math import atan2, degrees, pi


class Sprite_Mouse_Location(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)


class MyDialog:
    def __init__(self, parent, text):
        top = self.top = tk.Toplevel(parent)
        self.myLabel = tk.Label(
            top, text='Instrucciones para completar el nivel: ')
        self.myLabel.pack()

        self.myEntryBox = tk.Text(top, height=10, width=40)
        self.myEntryBox.insert('1.0', text)
        self.myEntryBox.pack()


class Game(object):
    def __init__(self, root, w, h):
        self.root = root
        self.width = w
        self.height = h
        self.root.title("CodeMonkey!")
        self.root.resizable(0, 0)

        # Tk init
        self.frame = tk.Frame(root, width=w, height=h)
        self.frame.pack(side=tk.LEFT)
        self.textLabelVariable = tk.StringVar()
        self.textLabelVariable.set('CodeMonkey! ... Nivel #' + str(0))
        self.label1 = tk.Label(root, textvariable=self.textLabelVariable)
        self.label1.configure(font=("Courier", 16, "italic"))
        self.label1.pack(pady=10)
        self.textBox1 = tk.Text(root, height=10, width=40)
        self.textBox1.pack(padx=30, pady=(20, 40), ipadx=10, ipady=60)
        self.button1 = tk.Button(
            root, text='Ejecutar', command=self.run_interpreter)
        self.button1.configure(relief=tk.GROOVE, borderwidth=5, background="sky blue",
                               activebackground="azure", highlightcolor="black")
        self.button1.configure(font=("Courier", 12, "bold", "roman"))
        self.button1.pack(ipadx=10, ipady=10)

        self.button2 = tk.Button(
            root, text='Repetir', command=self.repeat_level)
        self.button2.configure(relief=tk.GROOVE, borderwidth=5, background="sky blue",
                               activebackground="azure", highlightcolor="black")
        self.button2.configure(font=("Courier", 12, "bold", "roman"))
        self.button2.pack(ipadx=10, ipady=10, pady=(10, 0))

        self.button3 = tk.Button(
            root, text='Ayuda', command=self.instructions)
        self.button3.configure(relief=tk.GROOVE, borderwidth=5, background="sky blue",
                               activebackground="azure", highlightcolor="black")
        self.button3.configure(font=("Courier", 12, "bold", "roman"))
        self.button3.pack(ipadx=10, ipady=10, pady=(10, 0))

        root.update()

        # pygame init
        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((w, h))
        self.background = pygame.image.load(
            'resources/background_green.png').convert_alpha()

        # Creacion de personaje y objetos
        self.monkey = Monkey()

        # Create all the levels
        self.level_list = []
        self.level_list.append(Level_00(self.monkey))
        self.level_list.append(Level_01(self.monkey))
        self.level_list.append(Level_02(self.monkey))
        self.level_list.append(Level_03(self.monkey))
        self.level_list.append(Level_04(self.monkey))
        self.level_list.append(Level_05(self.monkey))
        self.level_list.append(Level_06(self.monkey))
        self.level_list.append(Level_07(self.monkey))
        self.level_list.append(Level_08(self.monkey))
        self.level_list.append(Level_09(self.monkey))

        # Set the current level
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        # Grupos de objetos
        self.active_sprite_list = pygame.sprite.Group()
        self.monkey.level = self.current_level

        self.active_sprite_list.add(self.monkey)

        # Control Interpreter
        self.control_movimiento = True
        self.steps = 0
        self.pox_y_actual_monkey = 0
        self.pox_x_actual_monkey = 0
        self.continuar = True
        self.lista_lineas = []
        self.move_control = False
        self.steps_auxiliary = 0
        self.instructions_levels = ''
        self.code_control = 0
        self.positivo = True
        self.move_turtle_monkey = False
        self.mouse_sprite = Sprite_Mouse_Location()
        self.objeto_a_mover_de_lista = []
        self.colision_rock = True

        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font("./resources/PeakCP.otf", 28)
        self.pos_x_font = 0
        self.pos_y_font = 0
        self.font_surface = self.font.render("", True, pygame.Color("white"))
        self.reset_values()
        self.game_loop()

    def read_txt(self):
        file1 = open("resources/instructions.txt", "r+")
        contador = 0
        for line in file1:
            if self.current_level_no == 0 and contador >= 2 and contador <= 5:
                self.instructions_levels += line
            elif self.current_level_no == 1 and contador >= 7 and contador <= 11:
                self.instructions_levels += line
            elif self.current_level_no == 2 and contador >= 13 and contador <= 20:
                self.instructions_levels += line
            elif self.current_level_no == 3 and contador >= 22 and contador <= 27:
                self.instructions_levels += line
            elif self.current_level_no == 4 and contador >= 29 and contador <= 34:
                self.instructions_levels += line
            elif self.current_level_no == 5 and contador >= 36 and contador <= 39:
                self.instructions_levels += line
            elif self.current_level_no == 6 and contador >= 41 and contador <= 45:
                self.instructions_levels += line
            elif self.current_level_no == 7 and contador >= 47 and contador <= 53:
                self.instructions_levels += line
            elif self.current_level_no == 8 and contador >= 55 and contador <= 64:
                self.instructions_levels += line
            elif self.current_level_no == 9 and contador >= 66 and contador <= 77:
                self.instructions_levels += line
            contador += 1
        file1.close()

    def instructions(self):
        self.instructions_levels = ''
        self.read_txt()
        MyDialog(self.root, self.instructions_levels)

    def reset_values(self):
        self.monkey.image = pygame.image.load(
            'resources/monkey.png').convert_alpha()
        self.monkey.angle = math.radians(-90)
        self.monkey.speed_x = 10 * math.cos(self.monkey.angle)
        self.monkey.speed_y = 10 * math.sin(self.monkey.angle)
        self.code_control = 0
        self.monkey.angulo_control = 0
        global_variable.bananas_type[:] = []
        global_variable.bananas_list[:] = []
        global_variable.turtles_type[:] = []
        global_variable.turtles_list[:] = []
        global_variable.crocodiles_type[:] = []
        global_variable.crocodiles_list[:] = []
        global_variable.matches_type[:] = []
        global_variable.matches_list[:] = []

        if self.current_level_no == 0:
            global_variable.bananas_type.append("bananas")
            global_variable.bananas_list.append(0)
            global_variable.bananas_list.append(1)
            global_variable.bananas_list.append(2)
            self.monkey.rect.x = 100
            self.monkey.rect.y = 350
            self.level_list[0] = Level_00(self.monkey)
        elif self.current_level_no == 1:
            global_variable.bananas_type.append("bananas")
            global_variable.bananas_list.append(0)
            global_variable.bananas_list.append(1)
            global_variable.bananas_list.append(2)
            global_variable.bananas_list.append(3)
            self.monkey.rect.x = 265
            self.monkey.rect.y = 265
            self.level_list[1] = Level_01(self.monkey)
        elif self.current_level_no == 2:
            global_variable.bananas_type.append("bananas")
            global_variable.bananas_list.append(0)
            global_variable.bananas_list.append(1)
            global_variable.turtles_type.append("turtles")
            global_variable.turtles_list.append(0)
            self.monkey.rect.x = 480
            self.monkey.rect.y = 500
            self.level_list[2] = Level_02(self.monkey)
        elif self.current_level_no == 3:
            global_variable.bananas_type.append("bananas")
            global_variable.bananas_list.append(0)
            global_variable.bananas_list.append(1)
            global_variable.bananas_list.append(2)
            self.monkey.rect.x = 80
            self.monkey.rect.y = 400
            self.level_list[3] = Level_03(self.monkey)
        elif self.current_level_no == 4:
            global_variable.bananas_type.append("bananas")
            global_variable.bananas_list.append(0)
            global_variable.bananas_list.append(1)
            global_variable.bananas_list.append(2)
            self.monkey.rect.x = 165
            self.monkey.rect.y = 460
            self.level_list[4] = Level_04(self.monkey)
        elif self.current_level_no == 5:
            global_variable.bananas_type.append("bananas")
            global_variable.bananas_list.append(0)
            global_variable.bananas_list.append(1)
            global_variable.bananas_list.append(2)
            global_variable.bananas_list.append(3)
            self.monkey.rect.x = 200
            self.monkey.rect.y = 365
            self.level_list[5] = Level_05(self.monkey)
        elif self.current_level_no == 6:
            self.monkey.rect.x = 80
            self.monkey.rect.y = 500
            self.level_list[6] = Level_06(self.monkey)
            global_variable.turtles_type.append("turtles")
            global_variable.turtles_list.append(0)
            global_variable.turtles_list.append(1)
            global_variable.turtles_list.append(2)
        elif self.current_level_no == 7:
            self.monkey.rect.x = 220
            self.monkey.rect.y = 460
            self.level_list[7] = Level_07(self.monkey)
            global_variable.bananas_type.append("bananas")
            global_variable.bananas_list.append(0)
            global_variable.bananas_list.append(1)
            global_variable.crocodiles_type.append("crocodiles")
            global_variable.crocodiles_list.append(0)
            global_variable.crocodiles_list.append(1)
        elif self.current_level_no == 8:
            self.monkey.image = pygame.image.load(
                'resources/mouse.png').convert_alpha()
            self.monkey.orig_image = self.monkey.image
            self.monkey.rect.x = 100
            self.monkey.rect.y = 250
            self.level_list[8] = Level_08(self.monkey)
            global_variable.matches_type.append("matches")
            global_variable.matches_list.append(0)
            global_variable.matches_list.append(1)
            global_variable.matches_list.append(2)
            global_variable.matches_list.append(3)
            global_variable.matches_list.append(4)
        elif self.current_level_no == 9:
            self.monkey.image = pygame.image.load(
                'resources/mouse.png').convert_alpha()
            self.monkey.orig_image = self.monkey.image
            self.monkey.rect.x = 100
            self.monkey.rect.y = 450
            self.level_list[9] = Level_09(self.monkey)
            global_variable.matches_type.append("matches")
            global_variable.matches_list.append(0)

    def repeat_level(self):
        self.lista_lineas = []
        global_variable.instructions_list = []
        self.code_control = 1
        self.move_control = False
        self.steps_auxiliary = 0
        self.continuar = True

    def game_loop(self):

        # Put labels
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.mouse_sprite.rect.x, self.mouse_sprite.rect.y = pygame.mouse.get_pos()
                for i in self.monkey.level.banana_list:
                    self.font_surface = self.font.render(
                        "", True, pygame.Color("black"))
                    if pygame.sprite.collide_rect(i, self.mouse_sprite):
                        self.pos_x_font = i.rect.x
                        self.pos_y_font = i.rect.y - 30
                        self.font_surface = self.font.render(
                            "banana[" + str(i.id) + "]", True, pygame.Color("black"))
                        break
                for i in self.monkey.level.turtle_list:
                    if pygame.sprite.collide_rect(i, self.mouse_sprite):
                        self.pos_x_font = i.rect.x
                        self.pos_y_font = i.rect.y - 30
                        self.font_surface = self.font.render(
                            "turtle[" + str(i.id) + "]", True, pygame.Color("black"))
                        break
                for i in self.monkey.level.beaver_list:
                    if pygame.sprite.collide_rect(i, self.mouse_sprite):
                        self.pos_x_font = i.rect.x
                        self.pos_y_font = i.rect.y - 30
                        self.font_surface = self.font.render(
                            "beaver[" + str(i.id) + "]", True, pygame.Color("black"))
                        break
                for i in self.monkey.level.crocodile_list:
                    if pygame.sprite.collide_rect(i, self.mouse_sprite):
                        self.pos_x_font = i.rect.x
                        self.pos_y_font = i.rect.y - 30
                        self.font_surface = self.font.render(
                            "crocodile[" + str(i.id) + "]", True, pygame.Color("black"))
                        break
                for i in self.monkey.level.match_list:
                    self.font_surface = self.font.render(
                        "", True, pygame.Color("black"))
                    if pygame.sprite.collide_rect(i, self.mouse_sprite):
                        self.pos_x_font = i.rect.x
                        self.pos_y_font = i.rect.y - 30
                        self.font_surface = self.font.render(
                            "match[" + str(i.id) + "]", True, pygame.Color("black"))
                        break

        # Auxiliar de próximo análisis sintáctico.
        if self.monkey.rect.y == (self.pox_y_actual_monkey - (self.steps * 10)):
            self.continuar = True
            self.pox_y_actual_monkey = self.monkey.rect.y
        if self.monkey.rect.y == (self.pox_y_actual_monkey + (self.steps * 10)):
            self.continuar = True
            self.pox_y_actual_monkey = self.monkey.rect.y
        if self.monkey.rect.x == (self.pox_x_actual_monkey - (self.steps * 10)):
            self.continuar = True
            self.pox_x_actual_monkey = self.monkey.rect.x
        if self.monkey.rect.x == (self.pox_x_actual_monkey + (self.steps * 10)):
            self.continuar = True
            self.pox_x_actual_monkey = self.monkey.rect.x

        # Proximo analisis del interprete
        if len(self.lista_lineas) != 0 and self.continuar == True:
            self.next_analysis()

        # Control de movimiento (Movimiento en pasos)
        if self.move_control == True:
            if self.steps_auxiliary != 0:
                if self.control_movimiento == True:
                    self.monkey.move_monkey(self.positivo)
                    if self.positivo:
                        self.steps_auxiliary -= 1
                    else:
                        self.steps_auxiliary += 1
                else:
                    if self.move_turtle_monkey == True:
                        self.monkey.rect.x -= 10
                        self.objeto_a_mover_de_lista[0].rect.x -= 10
                        self.steps_auxiliary -= 1
                    else:
                        self.objeto_a_mover_de_lista[0].move_block()
                        self.steps_auxiliary -= 1
            else:
                self.move_control = False
                self.continuar = True
                self.control_movimiento = True
                self.move_turtle_monkey = False

        # Control: Siguiente nivel, Repetir nivel, Juego terminado.
        if len(self.lista_lineas) == 0 and self.code_control == 1 and self.move_control == False:

            if len(self.monkey.level.banana_list) == 0 and len(self.monkey.level.match_list) == 0 and self.current_level_no < len(self.level_list)-1:
                messagebox.showinfo(
                    'Informacion', '¡Has ganado el nivel, adelante!')
                self.current_level_no += 1
                self.current_level = self.level_list[self.current_level_no]
                self.monkey.level = self.current_level
                self.textLabelVariable.set(
                    'CodeMonkey! ... Nivel #' + str(self.current_level_no))
                self.reset_values()
            elif (len(self.monkey.level.banana_list) != 0 and len(self.monkey.level.match_list) == 0
                    or len(self.monkey.level.banana_list) == 0 and len(self.monkey.level.match_list) != 0):
                messagebox.showinfo(
                    'Informacion', '¡Has perdido, el nivel se repetirá!')
                self.current_level = self.level_list[self.current_level_no]
                self.monkey.level = self.current_level
                self.reset_values()
            else:
                self.reset_values()
                messagebox.showinfo('Informacion', 'Juego terminado.')
                self.root.destroy()

        self.monkey.on = False
        # if the monkey collides with the turtle
        colisiones = pygame.sprite.spritecollide(
            self.monkey, self.monkey.level.turtle_list, False)    
        for i in colisiones:
            self.objeto_a_mover_de_lista = []
            self.objeto_a_mover_de_lista.append(i)
            self.monkey.on = True
            self.move_turtle_monkey = True

        # if the monkey collides with the bridge
        colisiones = pygame.sprite.spritecollide(
            self.monkey, self.monkey.level.bridge_list, False)    
        for i in colisiones:
            # Limites left y right de la colision
            if i.rect.x >= self.monkey.rect.x or i.rect.x <= self.monkey.rect.x:
                diferencia = abs(i.rect.x - self.monkey.rect.x)
                if diferencia <= 30:
                    self.monkey.on = True
        

        self.colision_rock = False
        # if the monkey collides with the rock
        colisiones = pygame.sprite.spritecollide(
            self.monkey, self.monkey.level.rock_list, False)    
        for i in colisiones:
            self.colision_rock = True
        # if the monkey collides with the beaver
        colisiones = pygame.sprite.spritecollide(
            self.monkey, self.monkey.level.beaver_list, False)    
        for i in colisiones:
            self.colision_rock = True
         # if the monkey collides with the crocodile
        colisiones = pygame.sprite.spritecollide(
            self.monkey, self.monkey.level.crocodile_list, False)    
        for i in colisiones:
            self.colision_rock = True

        if self.colision_rock == False and (self.current_level_no == 4 or self.current_level_no == 7):
            self.monkey.lives -= 1
            self.repeat_level() 

        # Control colision con rio
        colisiones2 = pygame.sprite.spritecollide(
            self.monkey, self.monkey.level.river_list, False)
        if self.monkey.on == False:
            for i in colisiones2:
                if i.rect.y <= self.monkey.rect.y:
                    diferencia = abs(i.rect.y - self.monkey.rect.y)
                    if diferencia < 90:
                        self.monkey.lives -= 1
                        self.repeat_level()
                elif i.rect.y >= self.monkey.rect.y:
                    diferencia = abs(i.rect.y - self.monkey.rect.y)
                    if diferencia < 60:
                        self.monkey.lives -= 1
                        self.repeat_level() 

        # Update the monkey
        self.active_sprite_list.update()

        # Update items in the level
        self.current_level.update()

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        self.current_level.draw(self.screen)
        self.active_sprite_list.draw(self.screen)

        self.screen.blit(self.font_surface, (self.pos_x_font, self.pos_y_font))

        pygame.display.flip()

        self.frame.after(100, self.game_loop)

    def run_interpreter(self):

        file1 = open("resources/code.txt", "w")
        self.text = self.textBox1.get('1.0', tk.END).splitlines()
        for line in self.text:
            file1.writelines(line + "\n")

        file1.close()

        fp = open("resources/code.txt", "r")
        source = fp.read()
        fp.close()

        try:
            res = p.get_parser().parse(source)

            for node in res.children:
                global_variable.instructions_list.append(node.eval())
            
            for i in global_variable.instructions_list:
                self.lista_lineas.append(i)
            
            self.code_control += 1
            
        except Exception as e:
            messagebox.showerror(
                    'Warning!', e.__class__.__name__ + ': ' + str(e))
        
    def next_analysis(self):

        Ingresar = True
        if isinstance(global_variable.instructions_list[0], tuple) or isinstance(global_variable.instructions_list[0], list):
            for i in global_variable.instructions_list[0]:
                if isinstance(i, tuple) or isinstance(i, list):
                    Ingresar = False
                    break
        
        if global_variable.instructions_list[0] != None and Ingresar == True:

            # Rotar
            if global_variable.instructions_list[0] == 'left':
                self.monkey.rote_monkey(90)
            elif global_variable.instructions_list[0] == 'right':
                self.monkey.rote_monkey(-90)
            elif isinstance(global_variable.instructions_list[0], int):
                self.monkey.rote_monkey(global_variable.instructions_list[0])
            elif global_variable.instructions_list[0] == 'say':
                messagebox.showinfo(
                    'Informacion', 'Hello World!!!')
            elif global_variable.instructions_list[0] == 'see':
                messagebox.showinfo(
                    'Informacion', 'Yes.')                
            elif global_variable.instructions_list[0] == 'health':
                messagebox.showinfo(
                    'Informacion', "Lives: " + str(self.monkey.lives))
            elif isinstance(global_variable.instructions_list[0], tuple) or isinstance(global_variable.instructions_list[0], list):
                if global_variable.instructions_list[0][1] == "Monkey":
                    if global_variable.instructions_list[0][0] > 0:
                        self.positivo = True
                    else:
                        self.positivo = False
                    self.steps = global_variable.instructions_list[0][0]
                    self.pox_y_actual_monkey = self.monkey.rect.y
                    self.pox_x_actual_monkey = self.monkey.rect.x
                    self.continuar = False
                    self.move_control = True
                    self.steps_auxiliary = self.steps
                    self.monkey.move_monkey(self.positivo)
                    self.control_movimiento = True
                elif global_variable.instructions_list[0][1] == "Turtle":
                        indice_avatar = global_variable.instructions_list[0][2]
                        self.objeto_a_mover_de_lista = []
                        for i in self.monkey.level.turtle_list:
                            if i.id == indice_avatar:
                                self.objeto_a_mover_de_lista.append(i)
                                self.steps = global_variable.instructions_list[0][0]
                                self.pox_y_actual = self.objeto_a_mover_de_lista[0].rect.y
                                self.pox_x_actual = self.objeto_a_mover_de_lista[0].rect.x
                                self.continuar = False
                                self.move_control = True
                                self.steps_auxiliary = self.steps
                                self.objeto_a_mover_de_lista[0].move_block()
                                self.control_movimiento = False
                                break
                elif global_variable.instructions_list[0][1] == "Beaver":
                        indice_avatar = global_variable.instructions_list[0][2]
                        self.objeto_a_mover_de_lista = []
                        for i in self.monkey.level.beaver_list:
                            if i.id == indice_avatar:
                                self.objeto_a_mover_de_lista.append(i)
                                self.steps = global_variable.instructions_list[0][0]
                                self.pox_y_actual = self.objeto_a_mover_de_lista[0].rect.y
                                self.pox_x_actual = self.objeto_a_mover_de_lista[0].rect.x
                                self.continuar = False
                                self.move_control = True
                                self.steps_auxiliary = self.steps
                                self.objeto_a_mover_de_lista[0].move_block()
                                self.control_movimiento = False
                                break

                elif global_variable.instructions_list[0][0] == "turnTo":
                    
                    if (len(global_variable.instructions_list[0])) == 4:
                        indice_avatar1 = global_variable.instructions_list[0][3]

                        objeto = []
                        for i in self.monkey.level.banana_list:
                            if i.id == indice_avatar1:
                                objeto.append(i)
                                break
                        
                        indice_avatar2 = global_variable.instructions_list[0][2]
                        objeto1 = []
                        for i in self.monkey.level.crocodile_list:
                            if i.id == indice_avatar2:
                                objeto1.append(i)
                                break
                        
                        dx = objeto1[0].rect.x - objeto[0].rect.x
                        dy = objeto1[0].rect.y - objeto[0].rect.y
                        if dy == 0:
                            dy = 1
                        angle = math.atan(float(dx)/float(dy))
                        angle *= 180/math.pi
                        if dy < 0:
                            angle += 180
                        if objeto1[0].angulo_control > 0:
                            objeto1[0].rotate_block(objeto1[0].angulo_control - angle)
                        else:
                            objeto1[0].rotate_block(objeto1[0].angulo_control + angle)
                        objeto1[0].angulo_control = 0
                    else:
                        
                        indice_avatar = global_variable.instructions_list[0][2]

                        if self.current_level_no <= 7:
                            objeto = []
                            for i in self.monkey.level.banana_list:
                                if i.id == indice_avatar:
                                    objeto.append(i)
                                    break
                        elif self.current_level_no >= 8:
                            objeto = []
                            for i in self.monkey.level.match_list:
                                if i.id == indice_avatar:
                                    objeto.append(i)
                                    break

                        dx = self.monkey.rect.x - objeto[0].rect.x
                        dy = self.monkey.rect.y - objeto[0].rect.y
                        if dy == 0:
                            dy = 1
                        angle = math.atan(float(dx)/float(dy))
                        angle *= 180/math.pi
                        if dy < 0:
                            angle += 180
                        if self.monkey.angulo_control > 0:
                            self.monkey.rote_monkey(self.monkey.angulo_control - angle)
                        else:
                            self.monkey.rote_monkey(self.monkey.angulo_control + angle)
                        self.monkey.angulo_control = 0
                        self.monkey.angle = math.radians(-90)
                elif global_variable.instructions_list[0][1] == "turtle":
                    indice_avatar = global_variable.instructions_list[0][0]
                    self.objeto_a_mover_de_lista = []
                    for i in self.monkey.level.turtle_list:
                        if i.id == indice_avatar:
                            self.objeto_a_mover_de_lista.append(i)
                            self.steps = global_variable.instructions_list[0][2]
                            self.pox_y_actual = self.objeto_a_mover_de_lista[0].rect.y
                            self.pox_x_actual = self.objeto_a_mover_de_lista[0].rect.x
                            self.continuar = False
                            self.move_control = True
                            self.steps_auxiliary = self.steps
                            self.objeto_a_mover_de_lista[0].move_block()
                            self.control_movimiento = False
                            break
                else:

                    tipo_avatar = global_variable.instructions_list[0][1]
                    indice_avatar = global_variable.instructions_list[0][0]

                    if self.current_level_no <= 7:
                        objeto = []
                        for i in self.monkey.level.banana_list:
                            if i.id == indice_avatar:
                                objeto.append(i)
                                break
                    elif self.current_level_no >= 8:
                            objeto = []
                            for i in self.monkey.level.match_list:
                                if i.id == indice_avatar:
                                    objeto.append(i)
                                    break

                    dist = math.hypot(self.monkey.rect.x - objeto[0].rect.x, self.monkey.rect.y - objeto[0].rect.y) / 10
                    
                    if dist > 0:
                        self.positivo = True
                    else:
                        self.positivo = False
                    self.steps = round(dist)
                    self.pox_y_actual_monkey = self.monkey.rect.y
                    self.pox_x_actual_monkey = self.monkey.rect.x
                    self.continuar = False
                    self.move_control = True
                    self.steps_auxiliary = self.steps
                    self.monkey.move_monkey(self.positivo)
                    self.control_movimiento = True

        global_variable.instructions_list.pop(0)
        self.lista_lineas.pop(0)

class Monkey(pygame.sprite.Sprite):
    '''Clase basica del mono'''

    def __init__(self):
        super().__init__()

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/monkey.png').convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(265, 265))
        self.continuar = True
        self.angulo_control = 0
        self.angle = math.radians(-90)
        self.speed_x = 10 * math.cos(self.angle)
        self.speed_y = 10 * math.sin(self.angle)
        self.on = False
        self.lives = 5
        self.level = None

    def move_monkey(self, positivo):
        if positivo:
            self.rect.x += round(self.speed_x)
            self.rect.y += round(self.speed_y)
        else:
            self.rect.x -= round(self.speed_x)
            self.rect.y -= round(self.speed_y)
    
    def rote_monkey(self, angulo):
        self.angulo_control += angulo
        self.image, self.rect = self.rotate(self.orig_image, self.rect, self.angulo_control)
        
        self.angle -= math.radians(angulo)
        self.speed_x = 10 * math.cos(self.angle)
        self.speed_y = 10 * math.sin(self.angle)
    
    def rotate(self, image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def update(self):

        # Control colision con match
        colisiones = pygame.sprite.spritecollide(
            self, self.level.match_list, False)
        for colision in colisiones:
            self.level.match_list.remove(colision)

        # Control colision con banana
        colisiones = pygame.sprite.spritecollide(
            self, self.level.banana_list, False)
        for colision in colisiones:
            self.level.banana_list.remove(colision)

        # Control colision con arbusto
        colisiones1 = pygame.sprite.spritecollide(
            self, self.level.bush_list, False)
        for colision in colisiones1:
            if self.rect.right < colision.rect.right:
                self.rect.right = colision.rect.left
            elif self.rect.left > colision.rect.left:
                self.rect.left = colision.rect.right
            elif self.rect.top > colision.rect.top:
                self.rect.top = colision.rect.bottom
            elif self.rect.bottom < colision.rect.bottom:
                self.rect.bottom = colision.rect.top
        
class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, id):
        super().__init__()
        self.image = pygame.image.load(imagen).convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(0, 0))
        self.continuar = True
        self.angulo_control = 0
        self.rect.x = x
        self.rect.y = y
        self.id = id
        self.velocidad = 10
    
    def move_block(self):
        self.rect.x -= self.velocidad
    
    def rotate_block(self, angulo):
        self.angulo_control += angulo
        self.image, self.rect = self.rotate(self.orig_image, self.rect, self.angulo_control)
        
    def rotate(self, image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

class Level(object):
    def __init__(self, monkey):
        self.banana_list = pygame.sprite.Group()
        self.bush_list = pygame.sprite.Group()
        self.match_list = pygame.sprite.Group()
        self.pile_list = pygame.sprite.Group()
        self.crocodile_list = pygame.sprite.Group()
        self.river_list = pygame.sprite.Group()
        self.rock_list = pygame.sprite.Group()
        self.bridge_list = pygame.sprite.Group()
        self.beaver_list = pygame.sprite.Group()
        self.turtle_list = pygame.sprite.Group()
        self.monkey = monkey
        self.background = pygame.image.load(
            'resources/background_green.png').convert_alpha()

    def update(self):
        self.match_list.update()
        self.pile_list.update()
        self.crocodile_list.update()
        self.river_list.update()
        self.bridge_list.update()
        self.rock_list.update()
        self.banana_list.update()
        self.bush_list.update()
        self.beaver_list.update()
        self.turtle_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw all the sprite lists that we have
        self.match_list.draw(screen)
        self.pile_list.draw(screen)
        self.crocodile_list.draw(screen)
        self.river_list.draw(screen)
        self.bridge_list.draw(screen)
        self.rock_list.draw(screen)
        self.beaver_list.draw(screen)
        self.turtle_list.draw(screen)
        self.banana_list.draw(screen)
        self.bush_list.draw(screen)

# Create platforms for the level
class Level_00(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        # Array with width, height, x, and y of platform
        banana = [[100, 40, "resources/banana.png", 0],
                 [450, 40, "resources/banana.png", 1],
                 [450, 350, "resources/banana.png", 2]
                 ]

        bush = [[300, 150, "resources/bush.png", ""],
                [300, 200, "resources/bush.png", ""],
                [300, 250, "resources/bush.png", ""],
                [300, 300, "resources/bush.png", ""],
                [300, 350, "resources/bush.png", ""]
                ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)

        # Go through the array above and add platforms
        for item in bush:
            bloque1 = Bloque(item[0], item[1], item[2], item[3])
            self.bush_list.add(bloque1)

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        # Array with width, height, x, and y of platform
        banana = [[265, 40, "resources/banana.png", 0],
                 [490, 265, "resources/banana.png", 1],
                 [265, 490, "resources/banana.png", 2],
                 [40, 265, "resources/banana.png", 3]
                 ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)

# Create platforms for the level
class Level_02(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_brown.jpg').convert_alpha()

        banana = [[180, 200, "resources/banana.png", 0],
                 [330, 200, "resources/banana.png", 1]
                 ]

        bush = [[100, 50, "resources/bush.png", ""],
                [100, 150, "resources/bush.png", ""],
                [100, 250, "resources/bush.png", ""],
                [250, 50, "resources/bush.png", ""],
                [250, 150, "resources/bush.png", ""],
                [250, 250, "resources/bush.png", ""],
                [400, 50, "resources/bush.png", ""],
                [400, 150, "resources/bush.png", ""],
                [400, 250, "resources/bush.png", ""]
                ]

        river = [[0, 300, "resources/river.png", ""]
                 ]
        
        turtle = [[430, 300, "resources/turtle.png", 0]
                 ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)

        # Go through the array above and add platforms
        for item in bush:
            bloque1 = Bloque(item[0], item[1], item[2], item[3])
            self.bush_list.add(bloque1)

        # Go through the array above and add platforms
        for item in river:
            bloque2 = Bloque(item[0], item[1], item[2], item[3])
            self.river_list.add(bloque2)

        # Go through the array above and add platforms
        for item in turtle:
            bloque2 = Bloque(item[0], item[1], item[2], item[3])
            self.turtle_list.add(bloque2)

# Create platforms for the level
class Level_03(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_brown.jpg').convert_alpha()

        # Array with width, height, x, and y of platform
        banana = [[80, 140, "resources/banana.png", 0],
                 [380, 140, "resources/banana.png", 1],
                 [380, 400, "resources/banana.png", 2]
                 ]
        
        river = [[0, 10, "resources/river.png", ""], 
                 [0, 200, "resources/river.png", ""]
                 ]
        
        bridge = [[80, 200, "resources/bridge.png", ""], 
                 [380, 200, "resources/bridge.png", ""]
                 ]
        
        bush = [[250, 300, "resources/bush.png", ""],
                [250, 360, "resources/bush.png", ""],
                [250, 420, "resources/bush.png", ""],
                [250, 480, "resources/bush.png", ""],
                [250, 540, "resources/bush.png", ""]
                ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)

        # Go through the array above and add platforms
        for item in river:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.river_list.add(bloque)

        # Go through the array above and add platforms
        for item in bridge:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.bridge_list.add(bloque)

        # Go through the array above and add platforms
        for item in bush:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.bush_list.add(bloque)

# Create platforms for the level
class Level_04(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_blue.jpg').convert_alpha()

        # Array with width, height, x, and y of platform
        banana = [[65, 40, "resources/banana.png", 0],
                 [165, 40, "resources/banana.png", 1],
                 [165, 250, "resources/banana.png", 2]
                 ]
        
        rock = [ [65, 40, "resources/rock.png", ""],
                 [165, 40, "resources/rock.png", ""],
                 [165, 110, "resources/rock.png", ""],
                 [165, 250, "resources/rock.png", ""],
                 [165, 390, "resources/rock.png", ""],
                 [165, 460, "resources/rock.png", ""],
                 ]
        
        beaver = [[400, 180, "resources/beaver.png", 0],
                 [400, 320, "resources/beaver.png", 1]
                 ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)

        # Go through the array above and add platforms
        for item in rock:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.rock_list.add(bloque)
        
        # Go through the array above and add platforms
        for item in beaver:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.beaver_list.add(bloque)

# Create platforms for the level
class Level_05(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_brown.jpg').convert_alpha()

        # Array with width, height, x, and y of platform
        banana = [ [80, 50, "resources/banana.png", 0],
                   [420, 50, "resources/banana.png", 1],
                   [260, 150, "resources/banana.png", 2],
                   [420, 250, "resources/banana.png", 3]
                 ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)

# Create platforms for the level
class Level_06(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_brown.jpg').convert_alpha()

        # Array with width, height, x, and y of platform
        banana = [[80, 10, "resources/banana.png", 0]
                 ]
        
        river = [[0, 70, "resources/river.png", ""],
                 [0, 220, "resources/river.png", ""],
                 [0, 370, "resources/river.png", ""]
                 ]
        
        turtle = [[430, 70, "resources/turtle.png", 0],
                  [430, 220, "resources/turtle.png", 1],
                  [430, 370, "resources/turtle.png", 2]
                 ]

        bush = [[250, 20, "resources/bush.png", ""],
                [250, 170, "resources/bush.png", ""],
                [250, 320, "resources/bush.png", ""]
                ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)
        
        # Go through the array above and add platforms
        for item in river:
            bloque2 = Bloque(item[0], item[1], item[2], item[3])
            self.river_list.add(bloque2)

        # Go through the array above and add platforms
        for item in turtle:
            bloque2 = Bloque(item[0], item[1], item[2], item[3])
            self.turtle_list.add(bloque2)

        # Go through the array above and add platforms
        for item in bush:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.bush_list.add(bloque)
 
# Create platforms for the level
class Level_07(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_blue.jpg').convert_alpha()

        # Array with width, height, x, and y of platform
        banana = [[390, 90, "resources/banana.png", 1],
                 [220, 250, "resources/banana.png", 0]
                 ]

        rock = [ [390, 90, "resources/rock.png", ""],
                 [220, 250, "resources/rock.png", ""],
                 [220, 460, "resources/rock.png", ""],
                 ]
        
        crocodile =[ [300, 120, "resources/crocodile.png", 0],
                    [220, 315, "resources/crocodile.png", 1]
                    ]

        # Go through the array above and add platforms
        for item in banana:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.banana_list.add(bloque)

        # Go through the array above and add platforms
        for item in rock:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.rock_list.add(bloque)

        # Go through the array above and add platforms
        for item in crocodile:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.crocodile_list.add(bloque)

# Create platforms for the level
class Level_08(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_yellow_solid.jpg').convert_alpha()

        # Array with width, height, x, and y of platform
        match = [[510, 260, "resources/match.png", 2],
                 [390, 180, "resources/match.png", 1],
                 [390, 340, "resources/match.png", 3],
                 [280, 40, "resources/match.png", 0],
                 [280, 490, "resources/match.png", 4]
                 ]
        
        pile = [[80, 400, "resources/pile.png", ""]
                 ]

        # Go through the array above and add platforms
        for item in match:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.match_list.add(bloque)
        
        # Go through the array above and add platforms
        for item in pile:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.pile_list.add(bloque)

# Create platforms for the level
class Level_09(Level):
    """ Definition for level 1. """

    def __init__(self, monkey):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, monkey)

        self.background = pygame.image.load(
            'resources/background_yellow_solid.jpg').convert_alpha()

        # Array with width, height, x, and y of platform
        match = [[500, 50, "resources/match.png", 0]
                 ]

        # Go through the array above and add platforms
        for item in match:
            bloque = Bloque(item[0], item[1], item[2], item[3])
            self.match_list.add(bloque)
        
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root, 600, 600)
    root.mainloop()

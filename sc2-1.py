from typing import List, Tuple
from sc2.bot_ai import BotAI                    # parent AI class to inherit from
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2 import maps
from sc2.position import Point2, Point3
from sc2.units import Unit
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
import random

class VAD3R_Bot(BotAI):    
    
    async def on_step(self, iteration:int):      # on_step is a method that is called every step of the game.
        print(f"The iteration is {iteration}")   # prints out the iteration number (ie: the step).
        
        await self.distribute_workers()
        first_attack = False

        def starport_land_positions(sp_position: Point2) -> List[Point2]:
            ''' Return all points that need to be checked when trying to land at a location where there is enough space to build an addon. Returns 13 points.'''
            land_positions = [(sp_position + Point2((x, y))).rounded for x in range(-1, 2) for y in range(-1, 2)]
            return land_positions + starport_points_to_build_addon(sp_position)


        def starport_points_to_build_addon(sp_position: Point2) -> List[Point2]:
            ''' Return all points that need to be checked when trying to build an addon. Returns 4 points. '''
            addon_offset: Point2 = Point2((2.5, -0.5))
            addon_position: Point2 = sp_position + addon_offset
            addon_points = [
                (addon_position + Point2((x - 0.5, y - 0.5))).rounded for x in range(0, 2) for y in range(0, 2)
            ]
            return addon_points        

        if self.townhalls:
            command_center = self.townhalls.random

            if self.supply_left > 0:
                for barrack in self.structures(UnitTypeId.BARRACKS).ready.idle:
                    if self.can_afford(UnitTypeId.MARINE) and self.units(UnitTypeId.MARINE).amount < 25:
                        barrack.train(UnitTypeId.MARINE)
                    else:
                        break
                    
                for factory in self.structures(UnitTypeId.FACTORY).ready.idle:
                    if self.can_afford(UnitTypeId.HELLION) and self.units(UnitTypeId.HELLION).amount < 5:
                        factory.train(UnitTypeId.HELLION)
                    else:
                        break
                        
                for port in self.structures(UnitTypeId.STARPORT).ready.idle:
                    if self.can_afford(UnitTypeId.BATTLECRUISER) and self.units(UnitTypeId.BATTLECRUISER).amount < 10 \
                       and self.structures(UnitTypeId.FUSIONCORE).ready:
                        port.train(UnitTypeId.BATTLECRUISER)
                    else:
                        break
    

            if command_center.is_idle and self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 22:
                command_center.train(UnitTypeId.SCV)
            
            elif self.structures(UnitTypeId.REFINERY).amount < 2:
                vespenes = self.vespene_geyser.closer_than(25, command_center)
                for vespene in vespenes:
                    if self.can_afford(UnitTypeId.REFINERY) and not self.already_pending(UnitTypeId.REFINERY):
                        await self.build(UnitTypeId.REFINERY, vespene)

            elif not self.structures(UnitTypeId.ENGINEERINGBAY):
                if self.can_afford(UnitTypeId.ENGINEERINGBAY):
                    await self.build(UnitTypeId.ENGINEERINGBAY, near=command_center)
            
            elif not self.already_pending(UnitTypeId.SUPPLYDEPOT) and self.can_afford(UnitTypeId.SUPPLYDEPOT) \
                and self.structures(UnitTypeId.SUPPLYDEPOT).amount < 14:
                await self.build(UnitTypeId.SUPPLYDEPOT,near=command_center.position.towards(self.game_info.map_center,16))
            
            elif self.structures(UnitTypeId.SUPPLYDEPOT).ready and self.structures(UnitTypeId.BARRACKS).amount < 2 \
                 and not self.already_pending(UnitTypeId.BARRACKS):
                if self.can_afford(UnitTypeId.BARRACKS):
                    await self.build(UnitTypeId.BARRACKS, near = command_center)
    

            elif self.structures(UnitTypeId.SUPPLYDEPOT).ready and self.structures(UnitTypeId.MISSILETURRET).amount < 4 \
                 and self.structures(UnitTypeId.BARRACKS).ready:
                if self.can_afford(UnitTypeId.MISSILETURRET) and not self.already_pending(UnitTypeId.MISSILETURRET):
                    await self.build(UnitTypeId.MISSILETURRET, near=self.structures(UnitTypeId.SUPPLYDEPOT).closest_to(command_center))
            
            elif self.structures(UnitTypeId.BARRACKS).ready and not self.structures(UnitTypeId.FACTORY) \
                 and not self.already_pending(UnitTypeId.FACTORY):
                if self.can_afford(UnitTypeId.FACTORY):
                    await self.build(UnitTypeId.FACTORY, near = command_center.position.towards(self.game_info.map_center,8))

            elif self.structures(UnitTypeId.BARRACKS).ready and self.structures(UnitTypeId.STARPORT).amount < 2 \
                 and not self.already_pending(UnitTypeId.STARPORT):
                if self.can_afford(UnitTypeId.STARPORT):
                    await self.build(UnitTypeId.STARPORT, near = command_center.position.towards(self.game_info.map_center,8))    
            
            elif self.structures(UnitTypeId.STARPORT).ready and not self.structures(UnitTypeId.FUSIONCORE) \
                and not self.already_pending(UnitTypeId.FUSIONCORE):
                if self.can_afford(UnitTypeId.FUSIONCORE):
                    await self.build(UnitTypeId.FUSIONCORE, near = command_center.position.towards(self.game_info.map_center,8))

            elif self.structures(UnitTypeId.FUSIONCORE).ready and self.structures(UnitTypeId.STARPORT).ready:

                # Build starport techlab or lift if no room to build techlab                
                sp: Unit
                for sp in self.structures(UnitTypeId.STARPORT).ready.idle:
                    if not sp.has_add_on and self.can_afford(UnitTypeId.STARPORTTECHLAB):
                        addon_points = starport_points_to_build_addon(sp.position)
                        if all(
                            self.in_map_bounds(addon_point) and self.in_placement_grid(addon_point)
                            and self.in_pathing_grid(addon_point) for addon_point in addon_points
                        ):
                            sp.build(UnitTypeId.STARPORTTECHLAB)
                        else:
                            sp(AbilityId.LIFT)           
            
                # Find a position to land for a flying starport so that it can build an addon
                for sp in self.structures(UnitTypeId.STARPORTFLYING).idle:
                    possible_land_positions_offset = sorted(
                        (Point2((x, y)) for x in range(-10, 10) for y in range(-10, 10)),
                        key=lambda point: point.x**2 + point.y**2,
                    )
                    offset_point: Point2 = Point2((-0.5, -0.5))
                    possible_land_positions = (sp.position.rounded + offset_point + p for p in possible_land_positions_offset)
                    for target_land_position in possible_land_positions:
                        land_and_addon_points: List[Point2] = starport_land_positions(target_land_position)
                        if all(
                            self.in_map_bounds(land_pos) and self.in_placement_grid(land_pos)
                            and self.in_pathing_grid(land_pos) for land_pos in land_and_addon_points
                        ):
                            sp(AbilityId.LAND, target_land_position)
                            break            
           
                         
 

            # Send workers back to mine if they are idle
            for scv in self.workers.idle :
                
                if self.structures(UnitTypeId.COMMANDCENTER).amount < 2 and self.can_afford(UnitTypeId.COMMANDCENTER)\
                and not self.already_pending(UnitTypeId.COMMANDCENTER) and self.units.amount > 50:
                    self.expand_now()
                
                for vs in self.vespene_geyser.closer_than(80,command_center):
                    scv.build_gas(target_geysir=vs)
                
                scv.gather(self.mineral_field.closest_to(command_center))


        else:
            if self.can_afford(UnitTypeId.COMMANDCENTER):
                await self.expand_now()
        

        if self.units(UnitTypeId.HELLION).amount >= 2 and  self.units(UnitTypeId.MARINE).amount >= 20\
             and self.units(UnitTypeId.BATTLECRUISER).amount >=4 and not first_attack:

            if self.enemy_units:
                for marine in self.units(UnitTypeId.MARINE).idle:
                    marine.attack(random.choice(self.enemy_units))
                for helion in self.units(UnitTypeId.HELLION).idle:
                    helion.attack(random.choice(self.enemy_units))
                for bc in self.units(UnitTypeId.BATTLECRUISER).idle:
                    bc.attack(random.choice(self.enemy_units))
                


            elif self.enemy_structures:
                for marine in self.units(UnitTypeId.MARINE).idle:
                    marine.attack(random.choice(self.enemy_structures))
                for helion in self.units(UnitTypeId.HELLION).idle:
                    helion.attack(random.choice(self.enemy_structures))
                for bc in self.units(UnitTypeId.BATTLECRUISER).idle:
                    bc.attack(random.choice(self.enemy_structures))
                    
                
            else:
                for marine in self.units(UnitTypeId.MARINE).idle:
                    marine.attack(self.enemy_start_locations[0])
                for helion in self.units(UnitTypeId.HELLION).idle:
                    helion.attack(self.enemy_start_locations[0])
                for bc in self.units(UnitTypeId.BATTLECRUISER).idle:
                    bc.attack(self.enemy_start_locations[0])

            first_attack = True

        elif first_attack == True and self.all_own_units.amount > 5:
            if self.structures(UnitTypeId.FUSIONCORE).ready.idle and self.structures(UnitTypeId.STARPORT).ready.idle:              
                    for fc in self.structures(UnitTypeId.FUSIONCORE):
                        fc.research(UpgradeId.BATTLECRUISERENABLESPECIALIZATIONS)

            for all_units in self.all_own_units:
                all_units.attack(random.choice(self.enemy_structures))
                all_units.attack(self.enemy_start_locations[0])
                all_units.attack(random.choice(self.all_enemy_units))   

run_game(                                         # run_game is a function that runs the game.
    maps.get("2000AtmospheresAIE"),               # the map we are playing on
    [Bot(Race.Terran, VAD3R_Bot()),               # runs our coded bot, terran race, and we pass our bot object 
     Computer(Race.Terran, Difficulty.Hard)],     # runs a pre-made computer agent, zerg race, with a Hard difficulty.
    realtime=False,                               # When set to True, the agent is limited in how long each step can take to process.
)
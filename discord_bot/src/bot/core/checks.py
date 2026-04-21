"""Permission and validation checks for Discord bot"""
import discord
from discord.ext import commands
from ..config import config
from typing import Callable


class ClockChecks:
    """Permission checks for clock commands"""
    
    @staticmethod
    def in_clock_channel():
        """Check if command is in the configured clock in/out channel"""
        async def predicate(ctx):
            # If no specific channel configured, allow anywhere
            if not config.INOUT_CHANNEL_ID:
                return True
            
            if str(ctx.channel.id) != config.INOUT_CHANNEL_ID:
                await ctx.send(
                    f"⛔ Clock commands only work in <#{config.INOUT_CHANNEL_ID}>"
                )
                return False
            return True
        return commands.check(predicate)
    
    @staticmethod
    def has_clock_role():
        """Check if user has the clock role"""
        async def predicate(ctx):
            if not config.CLOCK_ROLE_ID:
                return True  # No role required
            
            role = ctx.guild.get_role(int(config.CLOCK_ROLE_ID))
            if not role:
                await ctx.send("⚠️ Clock role not configured properly.")
                return False
            
            if role not in ctx.author.roles:
                await ctx.send("⛔ You need the Clock role to use time tracking.")
                return False
            return True
        return commands.check(predicate)
    
    @staticmethod
    def has_admin_role():
        """Check if user has the admin role"""
        async def predicate(ctx):
            # Check for admin permission first
            if ctx.author.guild_permissions.administrator:
                return True
            
            if not config.ADMIN_ROLE_ID:
                await ctx.send("⛔ Admin access required.")
                return False
            
            role = ctx.guild.get_role(int(config.ADMIN_ROLE_ID))
            if not role:
                await ctx.send("⚠️ Admin role not configured properly.")
                return False
            
            if role not in ctx.author.roles:
                await ctx.send("⛔ Admin access required.")
                return False
            return True
        return commands.check(predicate)
    
    @staticmethod
    async def is_admin(ctx) -> bool:
        """Check if user is admin (for help display)"""
        if ctx.author.guild_permissions.administrator:
            return True
        
        if not config.ADMIN_ROLE_ID:
            return False
        
        role = ctx.guild.get_role(int(config.ADMIN_ROLE_ID))
        if role and role in ctx.author.roles:
            return True
        return False

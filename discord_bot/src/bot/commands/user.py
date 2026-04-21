"""User Commands: in, out, pay, help"""
import discord
from discord.ext import commands
from ..core.checks import ClockChecks
from ..core.api_client import BackendAPIClient
from ..services.formatter import EmbedFormatter


class UserCommandHandler:
    """Handles all user-level !clock subcommands"""
    
    def __init__(self, bot: commands.Bot, api: BackendAPIClient, formatter: EmbedFormatter):
        self.bot = bot
        self.api = api
        self.formatter = formatter
    
    @ClockChecks.in_clock_channel()
    @ClockChecks.has_clock_role()
    async def in_(self, ctx: commands.Context, *args):
        """!clock in - Start work session"""
        user_id = str(ctx.author.id)
        
        try:
            # Check if already clocked in
            active = await self.api.get_active_session(user_id)
            if active:
                await ctx.send("❌ You are already clocked in!")
                return
            
            # Check agent health (90s rule)
            health = await self.api.check_agent_health(user_id)
            if not health.get('healthy'):
                seconds = health.get('seconds_since_heartbeat', 'unknown')
                await ctx.send(
                    f"❌ Desktop agent not detected (last heartbeat {seconds}s ago).\n"
                    f"Please launch the Time Tracker Agent and wait for it to show 'Connected'."
                )
                return
            
            # Start session
            session = await self.api.start_session(user_id)
            start_time = session.get('started_at', 'now')
            
            await ctx.send(
                f"✅ **Clocked in!**\n"
                f"Started at: {start_time}\n"
                f"Session ID: `{session.get('session_id')}`"
            )
            
        except Exception as e:
            await ctx.send(f"❌ Error clocking in: {str(e)}")
    
    @ClockChecks.in_clock_channel()
    async def out(self, ctx: commands.Context, *args):
        """!clock out - End work session"""
        user_id = str(ctx.author.id)
        
        try:
            # Get active session
            active = await self.api.get_active_session(user_id)
            if not active:
                await ctx.send("❌ You are not clocked in!")
                return
            
            # End session
            session_id = active['id']
            result = await self.api.end_session(session_id, user_id)
            
            hours = result.get('hours_worked', 0)
            minutes = result.get('minutes_worked', 0)
            
            await ctx.send(
                f"✅ **Clocked out!**\n"
                f"Session duration: {hours}h {minutes}m"
            )
            
        except Exception as e:
            await ctx.send(f"❌ Error clocking out: {str(e)}")
    
    async def pay(self, ctx: commands.Context, *args):
        """!clock pay - Show unpaid time and earnings"""
        user_id = str(ctx.author.id)
        
        try:
            summary = await self.api.get_pay_summary(user_id)
            
            embed = self.formatter.pay_summary_embed(ctx.author, summary)
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error getting pay summary: {str(e)}")
    
    async def show_help(self, ctx: commands.Context, *args):
        """!clock help - Show command help"""
        is_admin = await ClockChecks.is_admin(ctx)
        embed = self.formatter.help_embed(is_admin)
        await ctx.send(embed=embed)

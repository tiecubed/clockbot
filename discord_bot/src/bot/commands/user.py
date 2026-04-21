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
        """!clock in - Start work session (validates healthy agent)"""
        user_id = str(ctx.author.id)
        
        try:
            # Check if already clocked in
            active = await self.api.get_active_session(user_id)
            if active:
                await ctx.send("❌ You are already clocked in!")
                return
            
            # Check agent health (90s rule) - REQUIRED before clock in
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
            start_time = session.get('started_at_formatted', 'now')
            
            embed = discord.Embed(
                title="✅ Clocked In",
                description=f"Session started at {start_time}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Use !clock out when finished")
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error clocking in: {str(e)}")
    
    @ClockChecks.in_clock_channel()
    async def out(self, ctx: commands.Context, *args):
        """!clock out - End user's active session"""
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
            total_minutes = result.get('total_minutes', 0)
            
            embed = discord.Embed(
                title="✅ Clocked Out",
                color=discord.Color.green()
            )
            embed.add_field(name="Session Duration", value=f"{hours}h {minutes}m", inline=True)
            embed.add_field(name="Total Minutes", value=str(total_minutes), inline=True)
            embed.set_footer(text="Session saved and ready for payroll")
            await ctx.send(embed=embed)
            
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

"""Agent implementations — 23 specialized campaign agents."""

from htc_agents.agents.commander import CommanderAgent
from htc_agents.agents.scout import ScoutAgent
from htc_agents.agents.storyteller import StorytellerAgent
from htc_agents.agents.sentinel import SentinelAgent
from htc_agents.agents.connector import ConnectorAgent
from htc_agents.agents.builder import BuilderAgent
from htc_agents.agents.guardian import GuardianAgent
from htc_agents.agents.analyst import AnalystAgent
from htc_agents.agents.debate_coach import DebateCoachAgent
from htc_agents.agents.fundraiser import FundraiserAgent
from htc_agents.agents.scheduler import SchedulerAgent
from htc_agents.agents.pollster import PollsterAgent
from htc_agents.agents.media_coach import MediaCoachAgent
from htc_agents.agents.oppo_tracker import OppoTrackerAgent
from htc_agents.agents.ground_game import GroundGameAgent
from htc_agents.agents.crisis_manager import CrisisManagerAgent
from htc_agents.agents.speechwriter import SpeechwriterAgent
from htc_agents.agents.coalition_builder import CoalitionBuilderAgent
from htc_agents.agents.investigator import InvestigatorAgent
from htc_agents.agents.justice_tracker import JusticeTrackerAgent
from htc_agents.agents.data_engineer import DataEngineerAgent
from htc_agents.agents.community_liaison import CommunityLiaisonAgent
from htc_agents.agents.compliance_officer import ComplianceOfficerAgent
from htc_agents.agents.content_producer import ContentProducerAgent
from htc_agents.agents.fact_checker import FactCheckerAgent
from htc_agents.agents.researcher import ResearcherAgent

AGENTS = {
    "commander": CommanderAgent,
    "scout": ScoutAgent,
    "storyteller": StorytellerAgent,
    "sentinel": SentinelAgent,
    "connector": ConnectorAgent,
    "builder": BuilderAgent,
    "guardian": GuardianAgent,
    "analyst": AnalystAgent,
    "debate_coach": DebateCoachAgent,
    "fundraiser": FundraiserAgent,
    "scheduler": SchedulerAgent,
    "pollster": PollsterAgent,
    "media_coach": MediaCoachAgent,
    "oppo_tracker": OppoTrackerAgent,
    "ground_game": GroundGameAgent,
    "crisis_manager": CrisisManagerAgent,
    "speechwriter": SpeechwriterAgent,
    "coalition_builder": CoalitionBuilderAgent,
    "investigator": InvestigatorAgent,
    "justice_tracker": JusticeTrackerAgent,
    "data_engineer": DataEngineerAgent,
    "community_liaison": CommunityLiaisonAgent,
    "compliance_officer": ComplianceOfficerAgent,
    "content_producer": ContentProducerAgent,
    "fact_checker": FactCheckerAgent,
    "researcher": ResearcherAgent,
}

__all__ = [
    "CommanderAgent",
    "ScoutAgent",
    "StorytellerAgent",
    "SentinelAgent",
    "ConnectorAgent",
    "BuilderAgent",
    "GuardianAgent",
    "AnalystAgent",
    "DebateCoachAgent",
    "FundraiserAgent",
    "SchedulerAgent",
    "PollsterAgent",
    "MediaCoachAgent",
    "OppoTrackerAgent",
    "GroundGameAgent",
    "CrisisManagerAgent",
    "SpeechwriterAgent",
    "CoalitionBuilderAgent",
    "AGENTS",
]

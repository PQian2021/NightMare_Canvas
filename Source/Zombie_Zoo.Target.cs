// Made by Junye Qian

using UnrealBuildTool;
using System.Collections.Generic;

public class Zombie_ZooTarget : TargetRules
{
	public Zombie_ZooTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V2;

		ExtraModuleNames.AddRange( new string[] { "Zombie_Zoo" } );
	}
}

// Made by Junye Qian

using UnrealBuildTool;
using System.Collections.Generic;

public class Zombie_ZooEditorTarget : TargetRules
{
	public Zombie_ZooEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V2;

		ExtraModuleNames.AddRange( new string[] { "Zombie_Zoo" } );
	}
}

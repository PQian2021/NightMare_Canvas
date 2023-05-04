#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Runtime/Online/HTTP/Public/Http.h"
#include "MyHeartRateFetcher.generated.h"

UCLASS()
class ZOMBIE_ZOO_API AMyHeartRateFetcher : public AActor
{
public:
    GENERATED_BODY()

        AMyHeartRateFetcher();

    UPROPERTY(BlueprintReadOnly, Category = "HeartRate")
        int32 HeartRate;

protected:
    virtual void BeginPlay() override;

private:
    FHttpModule* Http;
    FTimerHandle FetchHeartRateTimerHandle;

    void FetchHeartRate();
    void OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);
};

#include "MyHeartRateFetcher.h"

AMyHeartRateFetcher::AMyHeartRateFetcher()
{
    PrimaryActorTick.bCanEverTick = false;
    Http = &FHttpModule::Get();
}

void AMyHeartRateFetcher::BeginPlay()
{
    Super::BeginPlay();
    GetWorld()->GetTimerManager().SetTimer(FetchHeartRateTimerHandle, this, &AMyHeartRateFetcher::FetchHeartRate, 1.0f, true);
}

void AMyHeartRateFetcher::FetchHeartRate()
{
    FString ApiURL = TEXT("http://127.0.0.1:5000/heart_rate");

    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
    Request->OnProcessRequestComplete().BindUObject(this, &AMyHeartRateFetcher::OnRequestComplete);
    Request->SetURL(ApiURL);
    Request->SetVerb("GET");
    Request->ProcessRequest();
}

void AMyHeartRateFetcher::OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
    if (bWasSuccessful && Response.IsValid())
    {
        TSharedPtr<FJsonObject> JsonObject;
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());
        if (FJsonSerializer::Deserialize(Reader, JsonObject))
        {
            if (JsonObject->HasTypedField<EJson::Number>("heart_rate"))
            {
                HeartRate = JsonObject->GetIntegerField("heart_rate");
                UE_LOG(LogTemp, Log, TEXT("Heart rate: %d"), HeartRate);
            }
        }
    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("Request failed"));
    }
}
